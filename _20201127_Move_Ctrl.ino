String stringOne; //create a string variable to hold inputed information
char charBuf[50]; //create a buffer to hold the characters and assign the buffer a max size [50]
int VarX; //integer variable
int VarT; //integer variable
int VarY;
int CPX; //current position in X
int EPX = 0; //entered position in X
int NMX = 0; //New movement in X
int NNMX = 0;
int CPY = 1; //current position in X
int EPY = 0; //entered position in X
int NMY = 0; //New movement in X
int NNMY = 0;
int Speed = 1900;
int SpeedY = 1900;
int SpeedZ = 1900;
int CPZ = 0; //current position in X
int EPZ = 0; //entered position in X
int NMZ = 0; //New movement in X
int NNMZ = 0;
int DPX = 0;
int StepsInY = 213;
int StepsInX =213;

boolean newData = false; 
boolean SendData = false;
boolean Xcomplete = false;
boolean Ycomplete = false;
boolean Zcomplete = false;

#define dirPinX 3
#define stepPinX 4
#define enPinX 2
#define stepsPerRevolution 200
#define dirPinY 6
#define stepPinY 5
#define enPinY 7 
#define dirPinZ 9
#define stepPinZ 8
#define enPinZ 10

void setup() {
  Serial.begin(9600); //establish interface with the serial monitor
  
  pinMode(stepPinX, OUTPUT); //set stepper motor pins
  pinMode(dirPinX, OUTPUT);
  pinMode(enPinX, OUTPUT);
  pinMode(stepPinY, OUTPUT);
  pinMode(dirPinY, OUTPUT);
  pinMode(enPinY, OUTPUT);
  pinMode(stepPinZ, OUTPUT);
  pinMode(dirPinZ, OUTPUT);
  pinMode(enPinZ, OUTPUT);
}

void loop() {

  recvString(); //receive the string from the Pi 
  prntString(); //convert the string into useable numbers
  blnk();  // interpret X coordinates and call movement functions
  blnkY();  //interpret Y coordinates and call movement functions
  blnkZ();  //interpret Z coordinates and call movement functions
  
 
  if (newData== true && Xcomplete == true && Ycomplete == true && Zcomplete == true){
    Serial.print("Movement complete");
    delay(100);
    
  }
  Xcomplete = false;
  Ycomplete = false;
  Zcomplete = false;
  newData = false; //reset newData so that the serial monitor doesn't continually print the old data


}

void recvString() { //function to receive data from the serial monitor

  while (Serial.available() > 0 && newData == false) { //look to see if new info has come through
    stringOne = Serial.readStringUntil('\n'); //read string until enter is pressed
    delay(100);
    Serial.flush();
    newData = true;
    //Serial.println(stringOne);
  }
}
void prntString() { //function to turn the string from the serial monitor into a series of characters
  if (newData == true) {

    
    stringOne.toCharArray(charBuf, 50) ; //command to turn string to characters

    int varX0 = (charBuf[0]-'0');
   

   //Serial.println(varX0);
    int VarX1 = (charBuf[1]-'0'); //changing character 1 (the second character) into an integer
   
    int VarX2 = (charBuf[2]-'0'); //changing character 2 (the third character) into an integer
    
    EPX = (10*VarX1)+(VarX2);
   
    int VarY = (charBuf[0]-'0'); //changing character 0 (the first character) into an integer
    
    EPY = varX0;
    
    
    delay(200);
  }
}

void blnk() //determine and record X movements 
{
  if (EPY >= 27 && newData==true)
  {
if (EPY == 27)
{ NMX= StepsInX;
moveMe();
CPX += 1;
delay(10);
//Serial.println(CPX);


}

if (EPY ==28 && newData==true){
  NMX = -1*StepsInX;
  moveMe();
  CPX -= 1;
  //Serial.println(CPX);
 
  
}
  }
  
  if (EPY < 27 && newData==true)
  {// a function to do some work if the second character is equal to a certain value
  NMX = StepsInX*(EPX - CPX); //calculation of X movement amount
  //Serial.println(NMX);
 CPX = CPX+(NMX/StepsInX); // setting new current  X position
//Serial.println(CPX);
   
  
moveMe();

}
else{
  Xcomplete = true;
}
}


void moveMe() {
   if (NMX  > 0 && newData == true) {
    // Set the spinning direction clockwise:
 digitalWrite(enPinX, HIGH);
  digitalWrite(dirPinX, HIGH);
  delay(5);
  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < NMX; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPinX, LOW);
    delayMicroseconds(Speed);
  }
 
   digitalWrite(enPinX, LOW);
   Xcomplete = true;
}
    

  
  if (NMX  < 0 && newData == true){
    
    int NegNMX = NMX*-1;
    NNMX=NegNMX;    
    //Serial.println(NNMX);
 
   digitalWrite(enPinX, HIGH);
  digitalWrite(dirPinX, LOW);
  delay(5);
{for (int b = 0; b < NNMX; b++){
  // Spin the stepper motor 1 revolution slowly:
  
    // These four lines result in 1 step:
    digitalWrite(stepPinX, HIGH);
    delayMicroseconds(Speed);
    digitalWrite(stepPinX, LOW);
    delayMicroseconds(Speed);
  }
  
 }
  digitalWrite(enPinX, LOW);
  Xcomplete = true;
}
else{
  Xcomplete = true;
}
}

void blnkY() //determine and record Y movements
{
  if (EPY >= 29 && newData==true)
  {
if (EPY == 29)
{ NMY= StepsInY;
moveMeY();
CPY += 1;
delay(10);
//Serial.println("I moved in Y");


}

if (EPY ==30 && newData==true){
  NMY = -1*StepsInY;
  moveMeY();
  CPY -= 1;
  //Serial.println(CPX);
 
  
}
  }
  
  if (EPY < 27 && newData==true)
  {// a function to do some work if the second character is equal to a certain value
  NMY = StepsInY*((EPY-16) - CPY); //calculation of X movement amount. Char A-'0' is equal to 17
  
 CPY = CPY+(NMY/StepsInY); // setting new current  X position
 //Serial.println(CPX);
   
  
moveMeY();

}
else{
  Ycomplete = true;
}
}


void moveMeY() {
   if (NMY  >= 0 && newData == true) {
    // Set the spinning direction clockwise:
 digitalWrite(enPinY, HIGH);
  digitalWrite(dirPinY, HIGH);
  delay(5);
  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < NMY; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPinY, HIGH);
    delayMicroseconds(SpeedY);
    digitalWrite(stepPinY, LOW);
    delayMicroseconds(SpeedY);
  }
 
   digitalWrite(enPinY, LOW);
   Ycomplete = true;
}
    

  
  if (NMY  < 0 && newData == true){
    
    int NegNMY = NMY*-1;
    NNMY=NegNMY;    
    
 
   digitalWrite(enPinY, HIGH);
  digitalWrite(dirPinY, LOW);
  delay(5);
{for (int b = 0; b <NNMY; b++){
  // Spin the stepper motor 1 revolution slowly:
  
    // These four lines result in 1 step:
    digitalWrite(stepPinY, HIGH);
    delayMicroseconds(SpeedY);
    digitalWrite(stepPinY, LOW);
    delayMicroseconds(SpeedY);
  }
  
 }
  digitalWrite(enPinY, LOW);
  Ycomplete = true;
}
else {
  Ycomplete = true;
}
}

void blnkZ() //determine and record Z movements
{
  if (EPY >= 32 && newData==true)
  {
if (EPY == 32)
{ NMZ= 10;
moveMeZ();
CPZ += 1;
delay(10);
//Serial.println("I moved in Y");


}

if (EPY ==33 && newData==true){
  NMZ = -10;
  moveMeZ();
  CPZ -= 1;
  //Serial.println(CPX);
 
  
}
  }
  else{
  Zcomplete = true;
}
}
   
  
void moveMeZ() {
   if (NMZ  >= 0 && newData == true) {
    // Set the spinning direction clockwise:
 digitalWrite(enPinZ, HIGH);
  digitalWrite(dirPinZ, HIGH);
  delay(5);
  // Spin the stepper motor 1 revolution slowly:
  for (int i = 0; i < NMZ; i++) {
    // These four lines result in 1 step:
    digitalWrite(stepPinZ, HIGH);
    delayMicroseconds(SpeedZ);
    digitalWrite(stepPinZ, LOW);
    delayMicroseconds(SpeedZ);
  }
 
   digitalWrite(enPinZ, LOW);
   Zcomplete = true;
}
    

  
  if (NMZ  < 0 && newData == true){
    
    int NegNMZ = NMZ*-1;
    NNMZ=NegNMZ;    
    
 
   digitalWrite(enPinZ, HIGH);
  digitalWrite(dirPinZ, LOW);
  delay(5);
{for (int b = 0; b <NNMZ; b++){
  // Spin the stepper motor 1 revolution slowly:
  
    // These four lines result in 1 step:
    digitalWrite(stepPinZ, HIGH);
    delayMicroseconds(SpeedZ);
    digitalWrite(stepPinZ, LOW);
    delayMicroseconds(SpeedZ);
  }
  
 }
  digitalWrite(enPinZ, LOW);
  Zcomplete = true;
}
else{
  Zcomplete = true;
}
}
