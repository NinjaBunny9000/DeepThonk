#include <FastLED.h>

#define DATA_PIN    3
#define LED_TYPE    WS2812B
#define COLOR_ORDER GRB
#define NUM_LEDS   96
CRGB leds[NUM_LEDS];

#define BRIGHTNESS          96
#define FRAMES_PER_SECOND  120

unsigned long lastcommand = 0;
unsigned long commandDuration = 10000;
unsigned long lastPeriodic = 0;
char incomingByte = ' ';


// SECTION Setup

void setup() {
  Serial.begin(9600);
  delay(3000); // 3 second delay for recovery
  
  // tell FastLED about the LED strip configuration
  FastLED.addLeds<LED_TYPE,DATA_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
  //FastLED.addLeds<LED_TYPE,DATA_PIN,CLK_PIN,COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);

  // set master brightness control
  FastLED.setBrightness(BRIGHTNESS);
}

// !SECTION 


// SECTION MAIN Loop

void loop()
{
  //periodic(300);
  if (Serial.available() > 0) {
	 // read the incoming byte:
	 incomingByte = Serial.read();
	 // Serial.print("I got: "); // ASCII printable characters
	 // Serial.println(char(incomingByte));
	 lastcommand = millis();
  }
  if (commandActive()) {
	 // weewoo();
	 switch (incomingByte) {
		case 'f':
		  commandDuration = 1500;
		  flashbang();
		  break;
		case 'w':
		
		  commandDuration = 5000;
		  weewoo();
		  break;
	 }
  }
  // else clearStrip();
  
  // send the 'leds' array out to the actual LED strip
  FastLED.show();  
  // insert a delay to keep the framerate modest
  FastLED.delay(1000/FRAMES_PER_SECOND); 
  fadeToBlackBy( leds, NUM_LEDS, 3);
}

// !SECTION 


// SECTION Function Definitions

bool commandActive() {
  return millis() - lastcommand < commandDuration;
}

void periodic(int period) {
  if (millis() > lastPeriodic + period) {
		sinewave();
		lastPeriodic = millis();
  }
}

void clearStrip(){
  for (int pos = 0; pos < NUM_LEDS; pos++) {
		leds[pos] = CRGB::Black;
  }
  // for (int pos = 0; pos < NUM_LEDS; pos++) {
  //     leds[pos].r = random8();
  //     leds[pos].g = random8();
  //     leds[pos].b = random8();
  // }
}

void sinewave() {
  int startingPos = random8(NUM_LEDS);
  int randHue = random8();
  for (int pos = 0; pos < 16 && pos + startingPos < NUM_LEDS; pos++) {
		leds[pos+startingPos] = CHSV(randHue, 255, sin8_avr(16*pos));
  }
}

void flashbang(){
  if (incomingByte == 'f'){
	for (int pos = 0; pos < NUM_LEDS; pos++) {
		leds[pos].setRGB( 200, 255, 255);
	}
	 // incomingByte = ' ';
  }
  
}

void weewoo() {

	for (int pos = 0; pos < NUM_LEDS; pos++) {
	 
	 if (pos < NUM_LEDS/2) {
		if (millis()%800>400) leds[pos] = CRGB::Red;
		else leds[pos] = CRGB::Blue;
	 }
	 else {  
		if (millis()%800>400) leds[pos] = CRGB::Blue;
		else leds[pos] = CRGB::Red;
	 }
  }
}

// !SECTION 