# Sistema de Inferencia On-Device y Control Inercial para Robot Móvil (ESP32 / MPU6050)

Arquitectura end-to-end para adquisición de señales inerciales, entrenamiento de un perceptrón multicapa (MLP) y despliegue de inferencia en tiempo real en microcontroladores ESP32, combinada con comunicación inalámbrica de baja latencia vía protocolo ESP-NOW.

---

## 📐 Pipeline de Procesamiento y Despliegue

El flujo del sistema se divide en los siguientes módulos de procesamiento y firmware:

1. **Adquisición Inercial e Interfaz I2C/Serial (`1_Lectura_del_sensor`):** Módulo de extracción de vector inercial de 6 DOF mediante MPU6050 a través de I2C, con puente de transmisión asíncrona vía Serial UART y Bluetooth (SPP).
2. **Captura Asíncrona de Muestras (`2_Recoleccion_de_datos`):** Pipeline en Python (`pyserial` + `threading` asíncrono e interfaz Tkinter) para registro continuo y serialización de tensores en formato `.npy`.
3. **Preprocesamiento y Estructuración (`3_Generar_dataset`):** Normalización z-score (`StandardScaler`) y codificación *One-Hot* de etiquetas. Consolidación de matrices de características $P \in \mathbb{R}^{N \times 3}$ y vectores de clase $T \in \mathbb{R}^{N \times 5}$.
4. **Modelado y Optimización (`4_Entrenamiento`):** Construcción de un Perceptrón Multicapa (Dense 3-2-5, ReLU/Softmax) en TensorFlow/Keras. Mapeo de matrices de pesos $W$ y vectores de sesgo $b$.
5. **Inferencia Embebida On-Device (`5_Prueba_red_neuronal`):** Implementación manual en C++ (Arduino Core) del forward-propagation para ejecución de inferencia directa en el ESP32 sin dependencias externas.
6. **Actuación y Diseño CAD (`6_Robot_movil_ESP32_NOW`):** Control de motores mediante puente H, esquemáticos de potencia y componentes CAD (.STL) para chasis e integración electrónica.
7. **Capa de Comunicación MAC/ESP-NOW (`7_Comunicacion_inalambrica`):** Vinculación punto a punto (P2P) de capa física de radiofrecuencia mediante direcciones MAC en modo Station/AP para reducir latencias frente a Wi-Fi tradicional.
8. **Validación y Calibración In-Situ (`8_Pruebas_experimentales`):** Rutinas de prueba experimental para mitigación de deriva inercial y ajuste de hiperparámetros en el microcontrolador.

---

## 📂 Estructura del Repositorio

```text
ESP32-Gesture-Robot/
├── 1_Lectura_del_sensor/          # Extracción I2C, streaming UART y transporte Bluetooth SPP
├── 2_Recoleccion_de_datos/        # Adquisición asíncrona multihilo en Python y GUI Tkinter
├── 3_Generar_dataset/             # Normalización matricial, One-Hot Encoding y tensores .npy
├── 4_Entrenamiento/               # Arquitectura MLP en Keras, funciones de pérdida y matrices W/b
├── 5_Prueba_red_neuronal/         # Forward propagation en C++ e inferencia embebida en ESP32
├── 6_Robot_movil_ESP32_NOW/       # Control PWM de motores, diagramas esquemáticos y archivos CAD (.STL)
├── 7_Comunicacion_inalambrica/    # Protocolo de comunicación P2P ESP-NOW y resolución de MAC
└── 8_Pruebas_experimentales/      # Calibración de drift del sensor y pruebas experimentales


🛠️ Stack Tecnológico
Firmware / C++: ESP32 Arduino Core, Wire.h (I2C), esp_now.h, BluetoothSerial.h.

Procesamiento y ML / Python: numpy, scikit-learn (StandardScaler), tensorflow.keras, matplotlib, pyserial.

CAD / Hardware: Archivos estereolitográficos (.STL) para chasis y soportes de electrónica/actuadores.

🎓 Créditos
Proyecto desarrollado para la asignatura Dispositivos Programables (Ingeniería Biomédica) en la Universidad Politécnica de Chiapas.
