#!/bin/bash
# Bash para instalar en Ubunutu server

echo "========================================================="
#Dar permiso de ejecuccion antes de ejecutar
# chmod +x instalacion.sh

# ejecutar
# ./instalacion.sh

echo "========================================================="
# Salir si ocurre algún error
set -e

echo "========================================================="
echo "1.- Actualizando el sistema..."
echo "========================================================="
sudo apt update && sudo apt upgrade -y

echo "========================================================="
echo "2.- Instalando Git..."
echo "========================================================="
sudo apt install git -y

echo "========================================================="
echo "3.- Instalando Python3 y pip..."
echo "========================================================="
sudo apt install python3 python3-pip -y

echo "========================================================="
echo "4.- Instalando python3-venv..."
echo "========================================================="
sudo pip3 install python3-venv -y

echo "========================================================="
echo "5.- Clonando el repositorio..."
echo "========================================================="
git clone https://github.com/H4RSHAD/proyecto-transcripcion.git

echo "========================================================="
echo "6.- Creando entorno virtual..."
echo "========================================================="
#mkdir -p ~/mi_proyecto
cd ~/proyecto-transcripcion
python3 -m venv venv


echo "========================================================="
echo "7.- Activando entorno virtual e instalando Flask..."
echo "========================================================="
source venv/bin/activate
pip install flask



echo "**********************************************************"
echo "Instalación completada."
echo "********************************************************"

