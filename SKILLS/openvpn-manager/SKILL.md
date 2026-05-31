---
name: openvpn-manager
description: Use when the user needs to manage OpenVPN connections for pentesting labs (HTB, TryHackMe, VulnHub, etc.). Knows how to connect, disconnect, verify VPN status, troubleshoot connectivity, and manage multiple VPN profiles.
---

# OpenVPN Manager

Guía para gestionar conexiones OpenVPN en el contexto de ciberseguridad ofensiva.

## Contexto del sistema

- **SO:** Arch Linux
- **OpenVPN:** Instalado vía `openvpn` package
- **Resolved:** systemd-resolved gestiona DNS
- **Las conexiones VPN requieren `sudo`** — el agente NUNCA ejecuta sudo directamente, solo muestra los comandos al usuario para que los ejecute manualmente.

## Ubicaciones comunes de archivos .ovpn

- `~/lab/htb/` — perfiles de Hack The Box
- `~/lab/thm/` — perfiles de TryHackMe
- `~/lab/vpn/` — otros perfiles de laboratorio
- Descargas recientes → `~/Downloads/*.ovpn`

## Comandos básicos

### Conectar OpenVPN (primer plano)
```bash
sudo openvpn ruta/al/perfil.ovpn
```
El comando queda en primer plano. Usar Ctrl+C para cortar.

### Conectar OpenVPN (segundo plano — daemon)
```bash
sudo openvpn --config ruta/al/perfil.ovpn --daemon
```
Recomendado cuando se necesita seguir trabajando en la misma terminal.

### Verificar conexión activa
```bash
ip a show tun0
```
Si `tun0` no existe, probar `ip a` para listar todas las interfaces. HTB suele crear `tun0`.

### Verificar ruta/routing
```bash
ip route
```
Verificar que la ruta a la VPN esté presente. HTB agrega rutas automáticas.

### Desconectar OpenVPN
```bash
sudo killall openvpn
```
o encontrar el PID:
```bash
pgrep -a openvpn
sudo kill <PID>
```

### Listar procesos OpenVPN activos
```bash
pgrep -a openvpn
```

## Hack The Box (HTB) — Flujo típico

1. Descargar el `.ovpn` desde la página de HTB (sección "Connect to HTB")
2. Guardarlo en `~/lab/htb/` o donde prefieras
3. Conectar:
   ```bash
   sudo openvpn --config ~/lab/htb/<nombre>.ovpn --daemon
   ```
4. Verificar conexión:
   ```bash
   ip a show tun0
   ```
5. Verificar IP asignada (la IP de tu máquina en HTB):
   ```bash
   ip a show tun0 | grep inet
   ```
6. Hacer ping a una máquina para probar conectividad:
   ```bash
   ping -c 2 10.10.x.x
   ```
7. Al terminar, desconectar:
   ```bash
   sudo killall openvpn
   ```

## TryHackMe (THM) — Flujo típico

Similar a HTB pero los .ovpn se descargan desde "Access" > "VPN" en la página de THM.
La interfaz suele ser `tun0` también.

## Troubleshooting común

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| `tun0` no aparece | No conectado o error en el .ovpn | Verificar `journalctl -u openvpn@ --no-pager` o ejecutar sin `--daemon` para ver errores |
| `Options error: Unrecognized option or missing parameter` | Versión de OpenVPN desactualizada | `sudo pacman -S openvpn` |
| `AUTH: Received error from server` | Credenciales inválidas o .ovpn expirado | Regenerar el .ovpn desde la plataforma |
| `Route already exists` | Conexión duplicada | Matar todas las instancias: `sudo killall openvpn` y reconectar |
| DNS no resuelve después de VPN | systemd-resolved conflicto | Verificar `/etc/resolv.conf` y probablemente reiniciar resolved: `sudo systemctl restart systemd-resolved` |

## Buenas prácticas

- **Siempre** verificar conectividad con `ping` después de conectar
- Usar `--daemon` para no bloquear la terminal
- Mantener los .ovpn organizados por plataforma
- No compartir los .ovpn (contienen credenciales)
- Los .ovpn expiran periódicamente en HTB/THM — regenerarlos si falla la autenticación
- Si se usa múltiples VPNs, verificar que las rutas no entren en conflicto con `ip route`
