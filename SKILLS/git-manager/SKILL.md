---
name: git-manager
description: Use when managing git repositories, branching, rebasing, stashing, hooks, bisect, worktrees, submodules, GPG signing, or resolving merge conflicts. Covers advanced git workflows for development and dotfiles management.
---

# git-manager

Guía práctica para git workflows, orientada a desarrollo de software y gestión de dotfiles.

## Contexto del usuario

- **Git config global:** `~/.gitconfig`
- **Repos principales:** `~/dotfiles/` (GitHub: D4rkDr4g0n/dotfiles), proyectos en `~/projects/`
- **Editor:** Neovim (LazyVim)
- **Firma de commits:** GPG key available via `secret-manager`
- **Plataforma:** GitHub (CLI: `gh`)

---

## 1. Configuración inicial

### .gitconfig recomendado
```ini
[user]
    name = Lucciano Campassi
    email = <tu-email>

[init]
    defaultBranch = main

[core]
    editor = nvim
    autocrlf = input
    whitespace = trailing-space,space-before-tab

[push]
    default = current
    autoSetupRemote = true

[fetch]
    prune = true

[rebase]
    autoSquash = true
    autoStash = true

[merge]
    conflictStyle = zdiff3

[log]
    date = iso

[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --decorate --all
    amend = commit --amend --no-edit
    unstage = reset HEAD --
    discard = restore .
    last = log -1 HEAD
    fixup = commit --fixup
    squash = commit --squash
    wip = commit -m "wip"
    bclean = "!f() { git branch --merged | grep -v \"*\" | grep -v \"main\\|master\" | xargs -r git branch -d; }; f"
```

### Configurar GPG signing
```bash
# Listar claves GPG
gpg --list-secret-keys --keyid-format=long

# Configurar firma para un repo específico
git config user.signingkey <KEY-ID>
git config commit.gpgSign true
git config tag.gpgSign true
```

---

## 2. Branching strategies

### GitHub Flow (recomendado para proyectos personales)
```bash
# Crear feature branch desde main
git checkout -b feature/descripcion-breve main

# Trabajar, commiter, pushear
git add -p
git commit -m "feat: descripción"
git push -u origin feature/descripcion-breve

# Crear PR via gh CLI
gh pr create --fill

# Mergear y eliminar branch remota
gh pr merge --squash
git branch -d feature/descripcion-breve
git push origin --delete feature/descripcion-breve
```

### Git Flow (para proyectos con releases)
```bash
# Inicializar
git flow init -d

# Feature
git flow feature start mi-feature
git flow feature finish mi-feature

# Release
git flow release start v1.2.0
git flow release finish v1.2.0

# Hotfix
git flow hotfix start v1.2.1
git flow hotfix finish v1.2.1
```

---

## 3. Commits atómicos y mensajes

### Conventional Commits
```
feat:     Nueva funcionalidad
fix:      Corrección de bug
docs:     Documentación
style:    Formato, linting (no cambia lógica)
refactor: Refactorización (no cambia comportamiento)
perf:     Mejora de rendimiento
test:     Tests
chore:    Mantenimiento, build, CI
ci:       Cambios en CI/CD
security: Parches de seguridad
```

### Commits interactivos
```bash
# Commit parcial (solo partes específicas de un archivo)
git add -p

# Fixup (marcar para squash en el commit anterior)
git commit --fixup <ref>
git rebase -i --autosquash HEAD~5

# Squash commits
git rebase -i HEAD~3
# cambiar "pick" por "squash" (o "s") en los que se quieran fusionar
```

---

## 4. Rebase interactivo

```bash
# Reordenar, editar, squash, drop commits
git rebase -i HEAD~10

# Rebase contra main
git rebase main

# Si hay conflictos durante rebase:
git status                    # Ver archivos en conflicto
git diff                      # Ver diferencias
# Resolver manualmente los conflictos, luego:
git add <archivo-resuelto>
git rebase --continue

# Abortar rebase si todo sale mal
git rebase --abort
```

---

## 5. Cherry-pick

```bash
# Traer commits específicos de otra branch a la actual
git cherry-pick <commit-hash>

# Múltiples commits
git cherry-pick <hash1> <hash2> <hash3>

# Sin hacer commit (para revisar primero)
git cherry-pick -n <commit-hash>

# Cherry-pick con opciones
git cherry-pick -x <hash>    # Agrega "(cherry picked from commit ...)" al mensaje
git cherry-pick -e <hash>    # Editar mensaje
```

---

## 6. Git Bisect — Búsqueda binaria de bugs

```bash
# Iniciar bisect
git bisect start
git bisect bad               # Commit actual tiene el bug
git bisect good <tag>        # Último commit conocido sin el bug

# Git te deja en un commit intermedio. Probar si el bug está:
# - Si sí: git bisect bad
# - Si no: git bisect good
# Repetir hasta encontrar el commit culpable

# Automatizar con script
git bisect start HEAD v1.0
git bisect run make test     # Script que retorna 0 (good) o non-zero (bad)

# Terminar
git bisect reset
```

---

## 7. Worktrees — Trabajo paralelo

```bash
# Crear worktree para una branch
git worktree add ../proyecto-feature feature/nueva-funcionalidad

# Crear worktree (y crear branch)
git worktree add -b feature/nueva-funcionalidad ../proyecto-feature main

# Listar worktrees
git worktree list

# Eliminar worktree
git worktree remove ../proyecto-feature

# Limpiar worktrees huérfanos (git >2.17)
git worktree prune
```

Útil cuando necesitás mantener la branch main limpia pero tener múltiples features en paralelo sin andar stashando constantemente.

---

## 8. Stashing

```bash
# Guardar cambios temporales
git stash

# Con mensaje descriptivo
git stash push -m "wip: refactor autenticación"

# Stash de archivos específicos
git stash push -m "solo config" -- src/config.rs

# Listar stashes
git stash list

# Aplicar stash
git stash pop                 # Aplica y elimina
git stash apply stash@{2}     # Aplica sin eliminar

# Crear branch desde stash
git stash branch feature/desde-stash stash@{0}

# Eliminar stash
git stash drop stash@{0}
git stash clear               # Eliminar TODOS (cuidado)
```

---

## 9. Resolución de conflictos

```bash
# Ver conflictos
git status
git diff                     # Muestra conflictos con marcadores
git diff --check             # Solo detecta conflict markers

# Estrategias
git checkout --ours <file>    # Quedarse con nuestra versión
git checkout --theirs <file>  # Quedarse con la versión entrante

# Merge drivers específicos
git merge -X ours <branch>
git merge -X theirs <branch>

# Ver conflictos con herramientas externas
git mergetool                 # Abre tu difftool configurado (nvim dift)
```

---

## 10. Hooks prácticos

### pre-commit — Detectar secrets/credenciales
```bash
#!/bin/sh
# .git/hooks/pre-commit
# Detectar posibles credenciales en archivos staged

git diff --cached --name-only | while read file; do
    if grep -qP '(?:password|secret|api.?key|token|credencial)\s*[:=]\s*["\x27]?[A-Za-z0-9_\-\.]{8,}' "$file" 2>/dev/null; then
        echo "ERROR: Posible credencial detectada en $file"
        echo "  Usa 'git unstage $file' si es accidental"
        exit 1
    fi
done
```

### commit-msg — Validar Conventional Commits
```bash
#!/bin/sh
# .git/hooks/commit-msg
# Validar formato Conventional Commit

COMMIT_MSG=$(cat "$1")
if ! echo "$COMMIT_MSG" | grep -qE '^(feat|fix|docs|style|refactor|perf|test|chore|ci|security|wip)(\(.+\))?: .{1,72}'; then
    echo "ERROR: El mensaje de commit no sigue Conventional Commits"
    echo "  Formato: tipo(alcance): descripción"
    echo "  Ejemplo: feat(auth): implementar login con OAuth2"
    exit 1
fi
```

### Instalar hooks automáticamente
```bash
# Por proyecto
cp hooks/pre-commit .git/hooks/
chmod +x .git/hooks/*

# Usando template global
git config --global init.templateDir ~/.git-templates
mkdir -p ~/.git-templates/hooks
cp hooks/* ~/.git-templates/hooks/
chmod +x ~/.git-templates/hooks/*
```

---

## 11. Submodules

```bash
# Agregar submodule
git submodule add https://github.com/user/repo.git libs/repo
git submodule init
git submodule update

# Clonar repo con submodules
git clone --recurse-submodules <url>

# Actualizar submodules
git submodule update --remote --merge

# Eliminar submodule
git submodule deinit -f libs/repo
rm -rf .git/modules/libs/repo
git rm -f libs/repo
```

---

## 12. Reflog — Recuperación ante desastres

```bash
# Ver historial de referencias (commit, reset, rebase, etc.)
git reflog

# Recuperar cambios "perdidos" tras un reset duro
git reflog
# Encontrar el commit previo al reset
git checkout -b recovered <hash-del-commit>

# Recuperar stash eliminado
git fsck --lost-found | grep commit | xargs git show
```

---

## 13. Logging y blame

```bash
# Log filtrado
git log --author="Lucciano"
git log --since="2 weeks ago"
git log -- libs/core.rs        # Commits de un archivo específico
git log -p -- src/             # Commits + diff de un directorio
git log --format="%h %s (%an, %ar)"

# Blame (último cambio de cada línea)
git blame src/main.py
git blame -L 50,100 src/main.py    # Solo líneas 50-100
git blame -w src/main.py           # Ignorar whitespace

# Shortlog (contribuciones por autor)
git shortlog -sn --since="2026-01-01"
```

---

## 14. Tags

```bash
# Crear tag
git tag v1.2.0                          # Ligero
git tag -a v1.2.0 -m "Release v1.2.0"  # Anotado (recomendado)
git tag -s v1.2.0 -m "Release v1.2.0"  # Firmado con GPG

# Push tags
git push origin v1.2.0
git push origin --tags                  # Todos los tags

# Listar
git tag -l "v1.*"
git tag --sort=-version:refname         # Últimos primero

# Eliminar
git tag -d v1.2.0
git push origin --delete v1.2.0
```

---

## 15. GitHub CLI (gh)

```bash
# Autenticación
gh auth login

# PRs
gh pr create --fill
gh pr create --title "feat: ..." --body "Descripción del cambio"
gh pr list --state open
gh pr checkout <number>

# Issues
gh issue create --label bug
gh issue list

# Repos
gh repo view D4rkDr4g0n/dotfiles
gh repo fork
gh repo sync

# Releases
gh release create v1.2.0 --title "v1.2.0" --notes "Notas del release"
gh release list
```

---

## 16. Estrategias para dotfiles

```bash
# Git bare repo (estrategia recomendada para dotfiles)
git init --bare ~/dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/dotfiles --work-tree=$HOME'
dotfiles config status.showUntrackedFiles no

# Agregar configs
dotfiles add ~/.config/nvim/init.lua
dotfiles commit -m "chore: agregar init.lua de nvim"
dotfiles push

# Clonar en nueva máquina
git clone --bare https://github.com/D4rkDr4g0n/dotfiles.git $HOME/dotfiles
alias dotfiles='/usr/bin/git --git-dir=$HOME/dotfiles --work-tree=$HOME'
dotfiles checkout
```

---

## 17. Buenas prácticas

1. **Commits atómicos** — un cambio lógico por commit, no "fix varios bugs"
2. **Mensajes claros** — Conventional Commits (feat:, fix:, chore:, etc.)
3. **Nunca pushear a main directo** — siempre usar branches y PRs
4. **Rebase antes de mergear** — mantener historial lineal
5. `.gitignore` temprano — evitar commiteo de basura (binarios, .env, __pycache__)
6. **Firmar commits con GPG** — especialmente en proyectos públicos y dotfiles
7. **No commiteo secrets** — usar pre-commit hooks + .gitignore + secret-manager
8. **Pull con rebase** — `git pull --rebase` en lugar de merge commits
9. **Bisect ante bugs** — no adivinar, usar búsqueda binaria
10. **Documentar en el README** — el `git log` no es documentación de usuario
