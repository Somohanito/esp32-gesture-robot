#include "WiFi.h"

//emisor : B8:D6:1A:40:EE:20
//receptor : B8:D6:1A:42:B3:64

void setup(){
  Serial.begin(115200);
  WiFi.mode(WIFI_MODE_STA);
  Serial.println(WiFi.macAddress());
}
 
void loop(){

}
