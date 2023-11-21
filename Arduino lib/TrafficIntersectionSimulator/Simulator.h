/* Traffic Intersection Simulator - Library to control André's Traffic Intersection Simulator
   Created By André Costa, 21st December 2020
*/

#ifndef Simulator_h
#define Simulator_h
#include "Arduino.h"
#include "HardwareSerial.h"

typedef enum
{
  NORTH = '0',
  WEST = '1',
  EAST = '2',
  SOUTH = '3',
  FREE_ZONE = '4',
}PositionEnum;
typedef enum
{
  RED = 'r',
  YELLOW = 'y',
  GREEN = 'g',
  TIMED_OUT = ' '
} ColorEnum;
typedef enum
{
  ENTRANCE = '0',
  EXIT = '1'
}LaneEnum;

class Simulator
{
  private:
    typedef enum
    {
      CONNECTED = 'k',
      SET = 'S',
      GET = 'G',
      NEW = 'N',
      PERMUTE = 'P',
      CAR = 'C',
      CIVILIAN = 'c',
      TRAFFIC_LIGHT = 'T',
      SIDE_WALK_LIGHT = 't'
    }ConnectionKeywordsEnum;
    
    #define TIME_BETWEEN_SENTS 50 // in ms
    #define TIME_OUT 10 // in ms

    HardwareSerial& _serial;
    bool _is_connected = false;
    unsigned long _sending_start_time;

  public:    
    //Constructor
    Simulator(HardwareSerial& serial);
    
    //Connection Status
    void begin(long baud);
    bool isConnected();
    bool canSend();

    //Traffic Lights
    void setTrafficLight(PositionEnum pos, ColorEnum color );
    void permuteTrafficLight(PositionEnum pos);
    ColorEnum getTrafficLight(PositionEnum pos);

    //SideWalk Lights
    void setSideWalkLight(PositionEnum pos, ColorEnum color);
    void permuteSideWalkLight(PositionEnum pos);
    ColorEnum getSideWalkLight(PositionEnum pos);

    //Cars
    int getNumberOfCarsInLane(PositionEnum pos);
    int getNumberOfCarsInLane(PositionEnum pos, LaneEnum lane);
    void addCar(PositionEnum start_pos, PositionEnum final_pos);

    //Civilians
    int getNumberOfCivilianInLane(PositionEnum pos);
    int getNumberOfCivilianInLane(PositionEnum pos,  PositionEnum lane);
    void addCivilian();
    
};
#endif