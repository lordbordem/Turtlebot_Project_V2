/* 
 * Git Sum Spaghetti
 * 
 * Arduino Button and Sound RosNode
 * 
 * MX2 Project Assignment 3
 * Last Modified 18th September
 */

#include "pitches.h"
#include <ros.h>
#include <std_msgs/Int8.h>


const int button_pin[] = {
  2, 3, 4, 5, 6};
bool last_reading[5];
long last_debounce_time[5];
long debounce_delay=50;
bool published[5];

int tone_dur = 50;
int buzzer = 9;

int melody = 0;

int bpm = 120;
int harmonic = 1;


void messageCb( const std_msgs::Int8& play_melody){
  melody = play_melody.data;
}

ros::NodeHandle nh;

std_msgs::Int8 pushed_msg;
ros::Publisher pub_button("pushed", &pushed_msg);
ros::Subscriber<std_msgs::Int8> sub("play_melody", &messageCb);

int pentatonic[5] = {NOTE_C4, NOTE_DS4, NOTE_F4, NOTE_G4, NOTE_AS4};

//TODO: Put these arrays in a seperate file and make a struct to store the size of the array (or figure out how to calculate the size of a passed array in a function)
float randomSong[][2] = {
  {
    NOTE_C4, 1    }
  ,
  {
    NOTE_D4, 1    }
  ,
  {
    NOTE_E4, 1    }
  ,
  {
    NOTE_F4, 1    }
};
int randomSongSize = sizeof(randomSong) / sizeof(randomSong[0]);

float chariots[][2] = {
  {
    REST, 2.5    }
  ,
  {
    NOTE_C4, 0.5    }
  ,
  {
    NOTE_F4, 0.33    }
  ,
  {
    NOTE_G4, 0.33    }
  ,
  {
    NOTE_A4, 0.34    }
  ,

  {
    NOTE_G4, 1    }
  ,
  {
    NOTE_E4, 1    }
  ,
  {
    REST, 0.5    }
  ,
  {
    NOTE_C4, 0.5    }
  ,
  {
    NOTE_F4, 0.33    }
  ,
  {
    NOTE_G4, 0.33    }
  ,
  {
    NOTE_A4, 0.34    }
  ,

  {
    NOTE_G4, 2    }
  ,
  {
    REST, 0.5    }
  ,
  {
    NOTE_C4, 0.5    }
  ,
  {
    NOTE_F4, 0.33    }
  ,
  {
    NOTE_G4, 0.33    }
  ,
  {
    NOTE_A4, 0.34    }
  ,

  {
    NOTE_G4, 1    }
  ,
  {
    NOTE_E4, 1    }
  ,
  {
    REST, 0.5    }
  ,
  {
    NOTE_E4, 0.5    }
  ,
  {
    NOTE_F4, 0.33    }
  ,
  {
    NOTE_E4, 0.33    }
  ,
  {
    NOTE_C4, 0.34    }
  ,

  {
    NOTE_C4, 2    }
  ,
  {
    REST, 2    }
  ,
};
int chariotsSize = sizeof(chariots) / sizeof(chariots[0]);

void setup()
{
  nh.initNode();
  nh.advertise(pub_button);
  nh.subscribe(sub);
  pinMode(13, OUTPUT);
  //initialise an input pin for our push button
  for (int i = 0; i < 5; i++) {
    pinMode(button_pin[i], INPUT);
    last_reading[i] = ! digitalRead(button_pin[i]);
    last_reading[i] = false;
    last_debounce_time[i] = 0;
    published[i] = true;
  }
}

void loop()
{
  switch (melody) {
    case(1):
    play(0, buzzer);
    melody = 0;
    break;
    case(2):
    play(1, buzzer);
    melody = 0;
    break;
    default:
    break;
  }

  int reading[5];
  int i;
  for (i = 0; i < 5; i++) {

    reading[i] = digitalRead(button_pin[i]);
    if (last_reading[i] != reading[i]){
      last_debounce_time[i] = millis();
      published[i] = false;

    }

    //if the button value has not changed for the debounce delay, we know its stable
    if ( !published[i] && (millis() - last_debounce_time[i])  > debounce_delay && reading[i] == HIGH) {
      int f = 0;
      switch(i) {
        case(0):
        f = 0.5*pentatonic[random(0,4)];
        break;
        case(1):
        f = pentatonic[random(0,4)];
        break;
        case(2):
        f = 2*pentatonic[random(0,4)];
        break;
        case(3):
        f = 4*pentatonic[random(0,4)];
        break;
        case(4):
        f = 8*pentatonic[random(0,4)];
        break;
      }
      tone(buzzer, f, tone_dur);
      delay(tone_dur);
      noTone(buzzer);
      digitalWrite(13, HIGH-digitalRead(13));
      pushed_msg.data = i + 1;
      pub_button.publish(&pushed_msg);
      published[i] = true;
    }

    last_reading[i] = reading[i];
  }


  nh.spinOnce();
}

void play(int a, int b) {
  if(a)
  {
     int s = 4;
    int currentMelody = melody;
    for (int thisNote = 0; thisNote < s; thisNote++) 
    {
      int noteDuration = (int) ((60000.0/bpm) * randomSong[thisNote][1]);
      tone(b, (int) harmonic*randomSong[thisNote][0], noteDuration);
      int pauseBetweenNotes = noteDuration * 1.30;
      unsigned long currentMillis = millis();
      while(millis() - currentMillis <= pauseBetweenNotes) {
      }
      //delay(pauseBetweenNotes);
      if (melody != currentMelody) {
        return;
      }
      noTone(b);
    }
  }
  else 
  {
    int s = 27;
    int currentMelody = melody;
    for (int thisNote = 0; thisNote < s; thisNote++) 
    {
      int noteDuration = (int) ((60000.0/bpm) * chariots[thisNote][1]);
      tone(b, (int) harmonic*chariots[thisNote][0], noteDuration);
      int pauseBetweenNotes = noteDuration * 1.30;
      unsigned long currentMillis = millis();
      while(millis() - currentMillis <= pauseBetweenNotes) {
        for (int i = 0; i < 5; i++) {
          if (digitalRead(button_pin[i])) {
            noTone(b);
            return;
          }
        }
      }
      //delay(pauseBetweenNotes);
      if (melody != currentMelody) {
        noTone(b);
        return;
      }
      noTone(b);
    }
  }  
  
}
