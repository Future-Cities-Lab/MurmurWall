import processing.serial.*;

Serial[] teensies = new Serial[7];
int[] b_rates = {9600,14400,19200,28800,38400,57600,115200};    

void setup() {
	println(Serial.list().length);
	for (int i = 0 ; i < Serial.list().length; i++) {
		println(Serial.list()[i]);
		//teensies[i] = new Serial(this, Serial.list()[i+11], b_rates[i]);
	}
}

void draw() {
	// for (int i = 0; i < teensies.length; i++) {
	// 	teensies[i].write(65);
	// }
	// for (int i = 0; i < teensies.length; i++) {
	// 	if (teensies[i].available() > 0) {
	// 		println(teensies[i].readStringUntil('\n'));
	// 	}
	// }

}