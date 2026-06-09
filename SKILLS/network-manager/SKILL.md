---
name: network-manager
description: Use when managing network configuration — nftables/iptables, WireGuard, bridges, VLANs, routing, DNS, network interfaces, traffic analysis, and network troubleshooting on Linux and Windows.
---

# network-manager

Guía de administración de redes para Linux y Windows. Cubre firewall, VPN site-to-site, bridges, VLANs, routing avanzado y troubleshooting. Complementa a atlas/hestia con networking profundo.

## Contexto del usuario

- **Linux:** Arch Linux (systemd-networkd, nftables, WireGuard)
- **Windows:** Windows 11 (Windows Firewall, WSL networking)
- **Hardware:** Placa de red interna + posiblemente interfaces USB
- **Uso:** Laboratorios de pentesting (HTB, THM), CSIRT, redes de VMs

---

## 1. WireGuard — VPN moderna

### Setup servidor
```bash
# Instalar
sudo pacman -S wireguard-tools

# Generar claves
wg genkey | tee /etc/wireguard/server.key | wg pubkey > /etc/wireguard/server.pub
chmod 600 /etc/wireguard/server.key

# Configuración — /etc/wireguard/wg0.conf
cat > /etc/wireguard/wg0.conf << 'EOF'
[Interface]
Address = 10.0.0.1/24
ListenPort = 51820
PrivateKey = <server-private-key>
# PostUp = iptables -A FORWARD -i wg0 -j ACCEPT
# PostDown = iptables -D FORWARD -i wg0 -j ACCEPT

[Peer]
# Cliente 1 — laptop
PublicKey = <client1-public-key>
AllowedIPs = 10.0.0.2/32
EOF
```

### Setup cliente
```bash
# /etc/wireguard/wg0.conf (cliente)
[Interface]
Address = 10.0.0.2/24
PrivateKey = <client-private-key>
DNS = 10.0.0.1

[Peer]
PublicKey = <server-public-key>
Endpoint = server.example.com:51820
AllowedIPs = 0.0.0.0/0, ::/0      # Full tunnel
PersistentKeepalive = 25
```

### Comandos de gestión
```bash
# Levantar/Bajar
sudo wg-quick up wg0
sudo wg-quick down wg0

# Ver estado
sudo wg show
sudo wg show wg0
sudo wg show wg0 transfer         # Datos transferidos
sudo wg show wg0 latest-handshakes

# systemd service
sudo systemctl enable --now wg-quick@wg0
```

### Troubleshooting WireGuard
```bash
# Logs
sudo journalctl -u wg-quick@wg0
sudo dmesg | grep wireguard

# Verificar puerto abierto
sudo ss -tulpn | grep 51820
sudo nft list ruleset | grep 51820

# Probar conectividad
ping -c 3 10.0.0.1
```

---

## 2. nftables — Firewall avanzado

```bash
# Ver reglas actuales
sudo nft list ruleset

# Tabla básica con reglas de estado
sudo nft -f /etc/nftables.conf

# Agregar reglas en vivo (sin editar archivo)
sudo nft add rule inet filter input tcp dport 2222 accept
sudo nft add rule inet filter input counter drop

# Eliminar regla (por handle)
sudo nft list ruleset -a                            # Ver handles
sudo nft delete rule inet filter input handle 3     # Eliminar por handle

# NAT (para forwarding de tráfico)
sudo nft add table ip nat
sudo nft add chain ip nat postrouting { type nat hook postrouting priority 100 \; }
sudo nft add rule ip nat postrouting oif eth0 masquerade
```

### Configuración completa
```bash
cat > /etc/nftables.conf << 'EOF'
table inet filter {
    chain input {
        type filter hook input priority 0; policy drop;
        
        # Loopback
        iif lo accept
        
        # Established/related
        ct state established,related accept
        
        # SSH (custom port)
        tcp dport 2222 accept
        
        # WireGuard
        udp dport 51820 accept
        
        # ICMP (limitado)
        ip protocol icmp icmp type { echo-request } limit rate 10/second accept
        
        # Logging
        log prefix "[NFT-BLOCK] " counter drop
    }
    
    chain forward {
        type filter hook forward priority 0; policy drop;
        
        # Forwarding para WireGuard
        iif wg0 accept
        oif wg0 accept
    }
    
    chain output {
        type filter hook output priority 0; policy accept;
    }
}

table inet nat {
    chain postrouting {
        type nat hook postrouting priority srcnat; policy accept;
        oif eth0 masquerade
    }
}
EOF
```

---

## 3. Bridges (para VMs/containers)

```bash
# Crear bridge (Linux bridge)
sudo ip link add name br0 type bridge
sudo ip link set br0 up

# Agregar interfaz física al bridge
sudo ip link set eth0 master br0

# Asignar IP al bridge
sudo ip addr add 192.168.1.100/24 dev br0

# Bridge persistente con systemd-networkd
# /etc/systemd/network/br0.netdev
[NetDev]
Name=br0
Kind=bridge

# /etc/systemd/network/br0.network
[Match]
Name=br0

[Network]
Address=192.168.1.100/24
Gateway=192.168.1.1
DNS=1.1.1.1

# /etc/systemd/network/eth0.network (esclava al bridge)
[Match]
Name=eth0

[Network]
Bridge=br0
```

### Docker bridge personalizado
```bash
# Crear red Docker con bridge personalizado
docker network create -d bridge \
  --subnet 172.20.0.0/16 \
  --ip-range 172.20.10.0/24 \
  --gateway 172.20.0.1 \
  lab-network

# Conectar contenedor a red específica
docker run --net lab-network --ip 172.20.10.5 -d nginx
```

---

## 4. VLANs

```bash
# Crear VLAN 100 sobre eth0
sudo ip link add link eth0 name eth0.100 type vlan id 100
sudo ip link set eth0.100 up
sudo ip addr add 10.0.100.1/24 dev eth0.100

# Con systemd-networkd
# /etc/systemd/network/eth0.100.netdev
[NetDev]
Name=eth0.100
Kind=vlan

[VLAN]
Id=100

# /etc/systemd/network/eth0.100.network
[Match]
Name=eth0.100

[Network]
Address=10.0.100.1/24
```

---

## 5. Rutas avanzadas

```bash
# Agregar ruta estática
sudo ip route add 10.0.0.0/8 via 192.168.1.1 dev eth0
sudo ip route add 172.16.0.0/12 via 192.168.1.1 dev eth0

# Ruta por defecto
sudo ip route add default via 192.168.1.1

# Tablas de rutas múltiples (policy routing)
echo "200 custom" >> /etc/iproute2/rt_tables
sudo ip rule add from 10.0.0.2 table custom
sudo ip route add default via 192.168.2.1 table custom

# Ver rutas
ip route show
ip route show table all
ip rule show
```

---

## 6. DNS y resolución

```bash
# systemd-resolved
resolvectl status
resolvectl query example.com

# DNS over TLS
# /etc/systemd/resolved.conf
[Resolve]
DNS=1.1.1.1 9.9.9.9
DNSOverTLS=yes
DNSSEC=allow-downgrade
Cache=yes

# Flush DNS cache
sudo resolvectl flush-caches

# Forzar servidor DNS específico por interfaz
sudo resolvectl dns wg0 10.0.0.1
sudo resolvectl domain wg0 "~lab.internal"
```

---

## 7. Network namespaces (para laboratorios)

```bash
# Crear namespace
sudo ip netns add lab-ns

# Ejecutar comando en namespace
sudo ip netns exec lab-ns ip addr
sudo ip netns exec lab-ns ping 8.8.8.8

# Conectar namespace al host con veth pair
sudo ip link add veth-host type veth peer name veth-lab
sudo ip link set veth-lab netns lab-ns
sudo ip addr add 10.0.1.1/24 dev veth-host
sudo ip netns exec lab-ns ip addr add 10.0.1.2/24 dev veth-lab
sudo ip link set veth-host up
sudo ip netns exec lab-ns ip link set veth-lab up
sudo ip netns exec lab-ns ip route add default via 10.0.1.1

# NAT desde host hacia el namespace
sudo nft add rule ip nat postrouting oif eth0 masquerade

# Listar namespaces
sudo ip netns list
```

---

## 8. Troubleshooting de red

```bash
# Conectividad básica
ping -c 4 8.8.8.8
ping -c 4 google.com

# Resolución DNS
dig +short google.com
nslookup google.com
host google.com

# Traceroute
traceroute -n 8.8.8.8
mtr 8.8.8.8  # Mejor (combina ping + traceroute en tiempo real)

# Puertos abiertos
ss -tulpn          # Listening
ss -tuna            # Conexiones establecidas
netstat -tulpn      # Alternativa

# Interfaces y ARP
ip addr
ip neigh
arp -a

# Captura de tráfico (básico)
sudo tcpdump -i eth0 port 443
sudo tcpdump -i wg0 -w /tmp/wg-capture.pcap

# Errores de interfaz
ip -s link show eth0  # RX/TX errors, drops
ethtool eth0           # Link status, speed, duplex

# Ancho de banda
sudo pacman -S iperf3
iperf3 -c server.example.com      # Test como cliente
iperf3 -s                          # Servidor de test
```

---

## 9. Windows Networking

```powershell
# Ver configuración de red
ipconfig /all
Get-NetIPConfiguration
Get-NetAdapter | Select Name, Status, LinkSpeed

# Rutas
route print
Get-NetRoute | Where DestinationPrefix -eq '0.0.0.0/0'

# DNS
Resolve-DnsName google.com
Clear-DnsClientCache

# Conexiones activas
Get-NetTCPConnection | Where State -eq 'Established'
Get-NetUDPEndpoint

# Firewall
Get-NetFirewallRule | Where Enabled -eq $true
New-NetFirewallRule -DisplayName "Allow WireGuard" -Direction Inbound -Protocol UDP -LocalPort 51820 -Action Allow

# WSL networking
wsl -- ip addr show eth0
wsl -- ping 8.8.8.8

# Reset de red (cuando todo falla)
netsh int ip reset
netsh winsock reset
ipconfig /release
ipconfig /renew
ipconfig /flushdns
```

---

## 10. Buenas prácticas

1. **Firewall default deny** — bloquear todo, permitir explícitamente
2. **WireGuard sobre OpenVPN** — más rápido, simple, seguro (para site-to-site)
3. **Documentar IPs** — mantener registro de asignaciones (en Obsidian)
4. **Separar tráfico** — VLANs o interfaces separadas para lab/producción
5. **DNS over TLS** — cifrar consultas DNS
6. **Logging de firewall** — auditar tráfico bloqueado periódicamente
7. **Namespaces** — para aislar tráfico de laboratorio del host
8. **Monitorear** — `bmon`, `nload`, `iftop` para ver tráfico en vivo
9. **Backup de configs** — nftables.conf, wg0.conf en dotfiles
10. **Testear conectividad** — después de cualquier cambio de red, verificar con ping + dig
