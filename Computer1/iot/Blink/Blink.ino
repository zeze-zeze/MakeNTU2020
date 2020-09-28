void setup() {
  Serial.begin(9600);
  pinMode(2, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(8, OUTPUT);
}

void loop() {
  delay(1000);
  if(Serial.available()){
    String line = Serial.readString();
    int id = line.substring(0, line.indexOf(",")).toInt();
    int finished = line.substring(line.indexOf(",") + 1).toInt();
    if(id == 0){
      if(finished > 80){
        digitalWrite(2, HIGH);
        digitalWrite(4, LOW);
      }
      else{
        digitalWrite(4, HIGH);
        digitalWrite(2, LOW);
      }
    }
    else if(id == 1){
      if(finished > 80){
        digitalWrite(6, HIGH);
        digitalWrite(8, LOW);
      }
      else{
        digitalWrite(8, HIGH);
        digitalWrite(6, LOW);
      }
    }
    /*char cstr[16];
    String(finished).toCharArray(cstr, 16);
    Serial.write(cstr);*/
  }
}
