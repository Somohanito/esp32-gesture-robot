# 🤖 Carrito Controlado por Gestos mediante Red Neuronal Embebida (ESP32)

Este repositorio contiene la arquitectura completa de software, scripts de procesamiento/entrenamiento y firmware embebido para un vehículo robótico controlado mediante gestos de la mano, utilizando un sensor **MPU6050** y una red neuronal ejecutada en tiempo real en un microcontrolador **ESP32**.

---

## 📐 Flujo de Trabajo del Proyecto

El sistema está estructurado por etapas secuenciales de desarrollo:

1. **Lectura del Sensor (`1_Lectura_del_sensor`):** Pruebas iniciales de comunicación I2C con el MPU6050 y transmisión vía Serial (USB) y Bluetooth.
2. **Recolección de Datos (`2_Recoleccion_de_datos`):** Interfaz en Python (`Tkinter` + `pyserial`) conectada al ESP32 para adquirir las señales inerciales y exportarlas a formato `.npy`.
3. **Generación del Dataset (`3_Generar_dataset`):** Consolidación, inspección visual y formateo de las muestras (`P.npy`) y etiquetas (`T.npy`) para 5 clases de gestos.
4. **Entrenamiento (`4_Entrenamiento`):** Construcción y entrenamiento de un modelo multiclase denso con Keras/TensorFlow. Exportación de pesos y matrices.
5. **Inferencia Embebida (`5_Prueba_red_neuronal`):** Implementación de la red neuronal directamente en C++ dentro del ESP32 para hacer clasificaciones locales.
6. **Robot Móvil & ESP-NOW (`6_Robot_movil_ESP32_NOW`):** Integración con el control de motores, esquemas de conexión y piezas para impresión 3D del chasis.
7. **Comunicación Inalámbrica (`7_Comunicacion_inalambrica`):** Vinculación punto a punto mediante protocolos de radiofrecuencia de baja latencia (ESP-NOW) y obtención de MAC Addresses.
8. **Pruebas Experimentales (`8_Pruebas_experimentales`):** Scripts de calibración fina y ensayos finales del vehículo en entorno real.

---

## 📂 Estructura del Repositorio

```text
ESP32-Gesture-Robot/
├── 1_Lectura_del_sensor/          # Pruebas básicas USB y Bluetooth del MPU6050
├── 2_Recoleccion_de_datos/        # GUI en Python y firmware para captura de muestras
├── 3_Generar_dataset/             # Scripts para unificar y visualizar matrices .npy
├── 4_Entrenamiento/               # Modelo Keras y exportación de pesos
├── 5_Prueba_red_neuronal/         # Red neuronal embebida corriendo en el ESP32
├── 6_Robot_movil_ESP32_NOW/       # Código del robot, diagrama eléctrico y modelos .STL 3D
├── 7_Comunicacion_inalambrica/    # Enlace emisor/receptor ESP-NOW y lectura MAC
└── 8_Pruebas_experimentales/      # Integración final de sensores y firmware de pruebas