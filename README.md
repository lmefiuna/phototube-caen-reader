# phototube-caen-reader
Programa de adquisición de datos y cómputo de energía asociada para el detector de muones por fototubo del Laboratorio de Mecánica y Energía de la FIUNA.

## Instalación

Asumiendo arquitectura `x64`. Para otras reemplazar por la correspondiente en los scripts *install* de `CAENVMElib` y `CAENComm`.

1. [`CAENUSBDrvB`](/CAENUSBdrvB-1.5.4/)

    ```bash
    CAENUSBdrvB-1.5.4$ sudo make && sudo make install
    ```

    Si sale un error de `Skipping BTF generation for /home/.... CAENUSBDrvB.ko due to unavailability of vmlinux`:

    ```bash
    sudo ln -sf /usr/lib/modules/`uname -r`/vmlinux.xz /boot/
    ```

    Referencia: [Skipping BTF generation xxx. due to unavailability of vmlinux on Ubuntu 21.04](https://askubuntu.com/a/1404795).

2. [`CAENVMElib`](/CAENVMELib-v3.4.4/)

    ```bash
    CAENVMELib-v3.4.4/lib$ sudo ./install_x64
    ```

3. [`CAENComm`](/CAENComm-v1.6.0/)

    ```bash
    CAENComm-v1.6.0/lib$ sudo ./install_x64
    ```

4. [`CAENDigitizer`](/CAENDigitizer-v2.17.3/). 



5. [`Wavedump`](/wavedump-3.10.6/). Es una versión modificada de la proveída en el [sitio web de CAEN](https://www.caen.it/products/caen-wavedump/). Requiere `gnuplot` (Instalar por `apt`, `yum` o similar).
    ```bash
    wavedump-3.10.6$ sudo ./configure
    wavedump-3.10.6$ sudo make && sudo make install
    ```

    Para recompilar:
    ```bash
    wavedump-3.10.6$ sudo make && sudo make install
    ```

## Configuración

Se requiere un archivo `config` en la raíz del directorio del proyecto con las siguientes especificaciones (todas las rutas deben ser absolutas):

```bash
# archivo de configuracion de los parametros del digitalizador
WAVEDUMP_CONFIG_FILE=/path/to/WaveDumpConfig.txt
# directorio de almacenamiento temporal de los datos recolectados. Debe existir previamente
WAVEDUMP_OUTPUT_PATH=/path/to/output/dir
# archivo de log
WATCHER_LOG_PATH=/path/to/file.log
# usuario e ip del servidor sql. En el programa se asume puerto por defecto 3306.
DATABASE_SERVER_HOST=username@123.456.789.321
# periodo de carga de datos en segundos
LOAD_PERIOD_SECONDS=15
# archivo csv temporal en el que se almacenan las energías de las ventanas de muestreo
CSV_OUTPUT_PATH=/path/to/file.csv
# ruta temporal en el servidor para alojar el archivo csv. Debe existir previamente
REMOTE_DIR_TMP=/tmp/
# usuario de base de datos
MYSQL_USER=user
# contrasenha de base de datos
MYSQL_PASSWORD=password
# base de datos a utilizar
MYSQL_DATABASE=muon_matrix
# tabla a utilizar
MYSQL_TABLE=phototube_energy
```

Si la tabla no está creada previamente:
```sql
-- mysql query
CREATE TABLE phototube_energy (
    timestamp INT(11) NOT NULL PRIMARY KEY UNIQUE,
    average_energy FLOAT NOT NULL
);
```

## Ejecución

```bash
phototube-caen-reader$ ./data_get.sh
```

Presionar `q` para detener la adquisición.