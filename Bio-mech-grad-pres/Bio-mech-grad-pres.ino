void setup() {
  Serial.begin(115200);
}

void loop() {
    int s1 = analogRead(A0);
   
/*  
    int s2 = analogRead(A1);
    int s3 = analogRead(A2);
    int s4 = analogRead(A3);
*/
    //Data needs to be send as "A12,B12,C12,D12;" where 12 is the value
    
    Serial.print("A");
    Serial.println(s1);
   /* Serial.print(",B");
    Serial.print(s2);
    Serial.print(",C");
    Serial.print(s3);
    Serial.print(",D");
    Serial.print(s4);
    Serial.println(";");*/
}
