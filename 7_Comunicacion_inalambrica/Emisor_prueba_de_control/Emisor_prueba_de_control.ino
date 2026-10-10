#include <esp_now.h>
#include <WiFi.h>

// REEMPLAZA CON LA Dirección MAC de tu receptor
uint8_t broadcastAddress[] = {0xB8, 0xD6, 0x1A, 0x42, 0xB3, 0x64};

// Variable para almacenar si el envío de datos fue exitoso
String success;

//Ejemplo de estructura para enviar datos
//Debe coincidir con la estructura del receptor
typedef struct struct_message {
    int control;
} struct_message;

struct_message comandos;

esp_now_peer_info_t peerInfo;

// Devolución de llamada cuando se envían datos
void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("\r\nEstado de envío del último paquete:\t");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Entrega exitosa" : "Error de entrega");
  if (status ==0){
    success = "Entrega exitosa :)";
  }
  else{
    success = "Error de entrega :(";
  }
}

///////////////////// COMUNICACION SERIAL ////////////////
String inputString = "";
bool stringComplete = false;

void setup() {
 // Inicializar monitor serie
  Serial.begin(115200);
 
  initEmisor();
  
}
 
void loop() {
  
  if(Serial.available()) serialEvent();

  ////////// SI RECIBE DATOS /////////////
  if (stringComplete) 
  {
    comandos.control = inputString.toInt();
    Serial.println(comandos.control);
    stringComplete = false;
    inputString = "";
  }

  // Enviar mensaje a través de ESP-NOW
  esp_err_t result = esp_now_send(broadcastAddress, (uint8_t *) &comandos, sizeof(comandos));
   
  if (result == ESP_OK) {
    Serial.println("Enviado con exito");
  }
  else {
    Serial.println("Error al enviar los datos");
  }

  delay(100);
}

/////////////// RECEPCION DE DATOS /////////////////////
void serialEvent() {
  while (Serial.available()) {
    
    char inChar = (char)Serial.read();
    inputString += inChar;
    
    if (inChar == '\n')
    {
      stringComplete = true;
    }
}
}


void initEmisor(){
   
   // Establecer el dispositivo como estación Wi-Fi
  WiFi.mode(WIFI_STA);

  // Iniciar ESP-AHORA
  if (esp_now_init() != ESP_OK) {
    Serial.println("Error al inicializar ESP-NOW");
    return;
  }

  // Una vez que ESPNow se inicie con éxito, nos registraremos en 
  // Enviar CB para obtener el estado del paquete transmitido
  esp_now_register_send_cb(OnDataSent);
  
  // Registrar par
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;
  
  // Agregar par      
  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Error al agregar par");
    return;
  }
}
