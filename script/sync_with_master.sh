#!/bin/bash

# sync_with_master.sh
# Este script sincroniza una rama con master y permite ingresar un mensaje de commit personalizado.

# USO:
# ./sync_with_master.sh nombre-de-tu-rama "Mensaje opcional de commit"
# Si no ingresas mensaje, se te pedirá escribirlo.

# -----------------------------

BRANCH=$1
COMMENT=$2

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # Sin color

if [ -z "$BRANCH" ]; then
  echo -e "${RED}❌ Debes especificar tu rama. Ejemplo: ./sync_with_master.sh feature/registrar-usuario${NC}"
  exit 1
fi

# Si no se proporcionó mensaje, pedirlo interactivamente
if [ -z "$COMMENT" ]; then
  read -p "📝 Ingresa el mensaje de commit: " COMMENT
fi

echo -e "${GREEN}🔄 Guardando cambios locales...${NC}"
git add .

# Commit con mensaje personalizado o por defecto si no hay cambios
git commit -m "$COMMENT" || echo -e "${GREEN}✅ No hay cambios para hacer commit.${NC}"

echo -e "${GREEN}📥 Cambiando a master y actualizando...${NC}"
git checkout master || { echo -e "${RED}❌ No se pudo cambiar a master.${NC}"; exit 1; }
git pull origin master || { echo -e "${RED}❌ No se pudo actualizar master desde origin.${NC}"; exit 1; }

echo -e "${GREEN}🔁 Volviendo a tu rama $BRANCH...${NC}"
git checkout "$BRANCH" || { echo -e "${RED}❌ No se pudo cambiar a la rama $BRANCH.${NC}"; exit 1; }

echo -e "${GREEN}🔗 Haciendo merge con master...${NC}"
git merge master || { echo -e "${RED}❌ Conflictos en el merge. Resuélvelos manualmente antes de continuar.${NC}"; exit 1; }

echo -e "${GREEN}📤 Subiendo cambios a tu rama...${NC}"
git push || { echo -e "${RED}❌ No se pudo hacer push a $BRANCH.${NC}"; exit 1; }

echo -e "${GREEN}✅ ¡Listo! Tu rama $BRANCH está actualizada con master.${NC}"
