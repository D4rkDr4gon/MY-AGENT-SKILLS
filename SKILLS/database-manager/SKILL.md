---
name: database-manager
description: Use when working with databases — SQLite, PostgreSQL, MariaDB. Covers queries, backups, migrations, optimization (EXPLAIN, indexes), dumps, restores, and administration tasks. Cross-platform (Linux + Windows).
---

# database-manager

Guía operativa de bases de datos para desarrollo y administración. Cubre SQLite y PostgreSQL — las dos que más probablemente uses en tu perfil.

## Contexto del usuario

- **SQLite:** Uso cotidiano (browsers, apps, herramientas CLI)
- **PostgreSQL:** Proyectos de desarrollo, laboratorios
- **Linux:** `sqlite3`, `psql` via pacman
- **Windows:** `sqlite3.exe`, `psql.exe` (si instalaste PostgreSQL)

---

## 1. SQLite

### Comandos básicos
```bash
# Abrir base de datos
sqlite3 database.db

# Comandos dentro del shell
sqlite> .tables                    # Listar tablas
sqlite> .schema                    # Ver esquema completo
sqlite> .schema table_name         # Esquema de una tabla
sqlite> .databases                 # Bases de datos abiertas
sqlite> .indexes                   # Índices
sqlite> .dump                      # Dump completo SQL
sqlite> .dump table_name           # Dump de una tabla
sqlite> .import file.csv table     # Importar CSV
sqlite> .headers on                # Mostrar headers
sqlite> .mode column               # Modo columnas
sqlite> .mode json                 # Output JSON
sqlite> .mode markdown             # Output markdown
sqlite> .output file.txt           # Output a archivo
sqlite> .exit                      # Salir
```

### Consultas útiles
```sql
-- Tamaño de las tablas
SELECT name, pgsize FROM dbstat ORDER BY pgsize DESC;

-- Optimización
PRAGMA page_count;
PRAGMA page_size;
PRAGMA freelist_count;
PRAGMA integrity_check;
PRAGMA quick_check;

-- Performance
PRAGMA synchronous = NORMAL;    -- Balance speed/safety (default FULL)
PRAGMA journal_mode = WAL;      -- Write-Ahead Log (mejor concurrencia)
PRAGMA cache_size = -64000;     -- 64MB de cache

-- Índices
CREATE INDEX idx_name ON users(name);
EXPLAIN QUERY PLAN SELECT * FROM users WHERE name = 'test';
```

### Backup y restauración
```bash
# Backup online (mientras se usa)
sqlite3 database.db ".backup backup.db"

# Dump SQL
sqlite3 database.db .dump > dump.sql
sqlite3 database.db .dump table_name > table_dump.sql

# Restore
sqlite3 new_database.db < dump.sql
sqlite3 new_database.db ".read dump.sql"

# Vaciar (recuperar espacio)
sqlite3 database.db "VACUUM;"
sqlite3 database.db "PRAGMA auto_vacuum = FULL; VACUUM;"
```

---

## 2. PostgreSQL

### Conexión
```bash
# Conectar a base de datos local
psql -U postgres -d mydatabase
psql -h localhost -U myuser -d mydb -p 5432

# Comandos dentro de psql
psql> \l                    # Listar databases
psql> \c dbname             # Conectarse a db
psql> \dt                   # Listar tablas
psql> \dt+                  # Tablas con detalles
psql> \d table_name         # Describir tabla (columnas, índices, constraints)
psql> \di                   # Listar índices
psql> \du                   # Listar usuarios/roles
psql> \dn                   # Listar schemas
psql> \df                   # Listar funciones
psql> \dv                   # Listar vistas
psql> \x                    # Modo expanded (vertical)
psql> \timing               # Mostrar tiempo de queries
psql> \o file.txt           # Output a archivo
psql> \i file.sql           # Ejecutar archivo SQL
psql> \q                    # Salir
```

### Consultas de administración
```sql
-- Bases de datos y tamaños
SELECT datname, pg_size_pretty(pg_database_size(datname))
FROM pg_database ORDER BY pg_database_size(datname) DESC;

-- Conexiones activas
SELECT pid, usename, application_name, client_addr, state, query
FROM pg_stat_activity WHERE state != 'idle';

-- Matar conexión
SELECT pg_terminate_backend(pid) FROM pg_stat_activity
WHERE usename = 'problematic_user';

-- Tamaño de tablas
SELECT relname, pg_size_pretty(pg_total_relation_size(relid))
FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC;

-- Tablas sin índices
SELECT schemaname, tablename
FROM pg_catalog.pg_tables
WHERE NOT EXISTS (
  SELECT 1 FROM pg_indexes WHERE tablename = pg_tables.tablename
) AND schemaname NOT IN ('pg_catalog', 'information_schema');
```

### Backup y restore
```bash
# Dump de base de datos completa
pg_dump -U postgres -d mydatabase > mydatabase.sql
pg_dump -U postgres -d mydatabase --inserts > mydatabase_inserts.sql

# Dump solo esquema (sin datos)
pg_dump -U postgres -d mydatabase --schema-only > schema.sql

# Dump solo datos (sin esquema)
pg_dump -U postgres -d mydatabase --data-only > data.sql

# Dump comprimido
pg_dump -U postgres -d mydatabase -Fc > mydatabase.dump

# Restore desde SQL
psql -U postgres -d mydatabase < mydatabase.sql

# Restore desde dump comprimido
pg_restore -U postgres -d mydatabase mydatabase.dump

# Dump de todas las databases
pg_dumpall -U postgres > all_databases.sql
```

### Performance y optimización
```sql
-- EXPLAIN ANALYZE (MOSTRAR PLAN DE EJECUCIÓN)
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- Ver queries lentas
SELECT query, calls, mean_time, rows
FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;
-- Nota: requiere pg_stat_statements extension activada

-- Índices recomendados
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
-- CONCURRENTLY = no bloquea escrituras durante creación

-- Buscar índices duplicados
SELECT pg_size_pretty(sum(pg_relation_size(idx))::bigint) as total,
  array_agg(idx) as indexes
FROM (
  SELECT indexrelid::regclass as idx, indrelid::regclass as tbl,
    (i.indrelid, i.indkey, i.indclass, i.indoption) as key
  FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid
) t GROUP BY tbl, key HAVING count(*) > 1;

-- Vacuum (recuperar espacio)
VACUUM (VERBOSE, ANALYZE) mydatabase;
VACUUM FULL mydatabase;  -- Bloqueante pero recupera más espacio
```

### Docker para PostgreSQL (lab)
```bash
# PostgreSQL en Docker para laboratorios
docker run -d --name pg-lab \
  -e POSTGRES_PASSWORD=changeme \
  -e POSTGRES_DB=labdb \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  postgres:16

# Conectarse
psql -h localhost -U postgres -d labdb
```

---

## 3. Buenas prácticas

1. **Siempre hacer backup antes de migraciones** — `pg_dump` o `.backup` en SQLite
2. **Índices en columnas de búsqueda/filtro** — pero no sobre-indexar (cada índice ralentiza writes)
3. **EXPLAIN ANALYZE antes de optimizar** — no adivinar cuellos de botella
4. **WAL mode en SQLite** para mejor concurrencia
5. **pg_stat_statements** en PostgreSQL para monitorear queries lentas
6. **Migraciones con transacciones** — `BEGIN; ... ; ROLLBACK;` si algo falla
7. **No exponer PostgreSQL a internet** — usar SSH tunnel o Docker con red interna
8. **Passwords fuertes** — no usar `postgres:postgres` ni siquiera en lab
9. **Vacuum periódico** en PostgreSQL para salud de la base
10. **SQLite para datos locales/embebidos**, PostgreSQL para servidores multi-usuario
