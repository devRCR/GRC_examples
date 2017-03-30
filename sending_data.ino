#include <SPI.h>
#include <RH_RF22.h>

uint8_t fhch  = 4;
uint8_t fhs   = 20;

// Singleton instance of the radio driver
RH_RF22 rf22;

void setup() 
{
  Serial.begin(9600);
  if (!rf22.init())
    Serial.println("init failed");
  // Configurando parámetros de modulación
  rf22.setFrequency(915.0);
  rf22.setFHChannel(fhch);        // true if the selected frquency centre + (fhch * fhs) is within range 
  rf22.setFHStepSize(fhs);        // Frequency Hopping step size in 10kHz increments
  rf22.setModemConfig(RH_RF22::GFSK_Rb2_4Fd36);
  rf22.setTxPower(RH_RF22_TXPOW_14DBM);
}

void loop()
{
  Serial.println("Sending to BladeRF");
  // Enviando un mensaje al BladeRF
  char data[] = "Canal 4";
  for (int i=0; i<sizeof(data);i++){
  Serial.print(data[i]);
  }
  Serial.println();
  rf22.send(data, sizeof(data));
  rf22.waitPacketSent(); // espera a que el paquete haya sido enviado.

  delay(2000);
}
