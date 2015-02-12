import processing.serial.*;

private int NUM_MATRICES = 7;
private String[] teensies = new String[NUM_MATRICES];
private Serial[] teensy_serial = new Serial[NUM_MATRICES];
private String[] usb_ports = {"688851","616481","618061","688531","688321","688291","604971"};


void setup() {
	for (int i = 0; i < NUM_MATRICES; i++) {
		teensies[i] = Serial.list()[Serial.list().length-1-i];
	}

	for (int i = 0; i < NUM_MATRICES; i++) {
		String to_find = usb_ports[i];
		String port = "";
		for (int j = 0; j < NUM_MATRICES; j++) {
			if (teensies[j].contains(to_find)) {
				teensy_serial[i] = new Serial(this, teensies[j], 9600);
				teensy_serial[i].bufferUntil('\n');
			}
		}
	}

}

void draw() {
	for (int i = 0; i < NUM_MATRICES; i++) {
		println("Writting to " + teensy_serial[i].toString());
		teensy_serial[i].write(65);
		delay(10000);
	}
}

void serialEvent(Serial p) { 
	String val = p.readStringUntil('\n');
	println(val); 
	p.clear();
} 