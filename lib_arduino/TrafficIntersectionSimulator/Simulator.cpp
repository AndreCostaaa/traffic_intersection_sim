/* Traffic Intersection Simulator - Library to control André's Traffic Intersection Simulator
   Created By André Costa, 21st December 2020
*/

#include "Simulator.h"
#include "HardwareSerial.h"

Simulator::Simulator(HardwareSerial& serial):
    _serial(serial)
{
  	_sending_start_time = 0;
    _is_connected = false;
}
void Simulator::begin(long baud)
{
    _serial.begin(baud);
}
bool Simulator::isConnected()
{
  if (_serial.available() > 0)
  {
    if (_serial.read() == CONNECTED)
    {
      _is_connected = true;
    }
  }
  return _is_connected;
}
bool Simulator::canSend()
{
    return millis() - _sending_start_time >= TIME_BETWEEN_SENTS;
}
void Simulator::setTrafficLight(PositionEnum pos, ColorEnum color )
{
    _serial.write(Simulator::SET);
    _serial.write(Simulator::TRAFFIC_LIGHT);
    _serial.write(pos);
    _serial.write(color);
    _serial.println();
    _sending_start_time = millis();
}
void Simulator::permuteTrafficLight(PositionEnum pos)
{
	_serial.write(Simulator::PERMUTE);
	_serial.write(Simulator::TRAFFIC_LIGHT);
   	_serial.write(pos);
    _serial.println();
   	_sending_start_time = millis();

}
ColorEnum Simulator::getTrafficLight(PositionEnum pos)
{
    _serial.write(GET);
    _serial.write(TRAFFIC_LIGHT);
    _serial.write(pos);
    _serial.println();
    _sending_start_time = millis();
    while(!_serial.available())
    {
    	if(millis() - _sending_start_time >= TIME_OUT)
    	{
    		return TIMED_OUT;
    	}
    }
    return (ColorEnum)_serial.read();
}
void Simulator::setSideWalkLight(PositionEnum pos, ColorEnum color )
{
    _serial.write(Simulator::SET);
    _serial.write(Simulator::SIDE_WALK_LIGHT);
    _serial.write(pos);
    _serial.write(color);
    _serial.println();
    _sending_start_time = millis();
}
void Simulator::permuteSideWalkLight(PositionEnum pos)
{
	_serial.write(Simulator::PERMUTE);
	_serial.write(Simulator::SIDE_WALK_LIGHT);
   	_serial.write(pos);
    _serial.println();
   	_sending_start_time = millis();
}
ColorEnum Simulator::getSideWalkLight(PositionEnum pos)
{
    _serial.write(Simulator::GET);
    _serial.write(Simulator::SIDE_WALK_LIGHT);
    _serial.write(pos);
    _serial.println();
    _sending_start_time = millis();
    while(!_serial.available())
    {
    	if(millis() - _sending_start_time >= TIME_OUT)
    	{
    		return TIMED_OUT;
    	}
    }
    return (ColorEnum)_serial.read();
}

int Simulator::getNumberOfCarsInLane(PositionEnum pos)
{
	_serial.write(Simulator::GET);
    _serial.write(Simulator::CAR);
    _serial.write(pos);
    _serial.println();
    _sending_start_time = millis();
    while(!_serial.available())
    {
    	if(millis() - _sending_start_time >= TIME_OUT)
    	{
    		return -1;
    	}
    }
    return _serial.read() - '0';
}
int Simulator::getNumberOfCarsInLane(PositionEnum pos, LaneEnum lane)
{
	_serial.write(Simulator::GET);
    _serial.write(Simulator::CAR);
    _serial.write(pos);
    _serial.write(lane);
    _serial.println();
    _sending_start_time = millis();
    while(!_serial.available())
    {
    	if(millis() - _sending_start_time >= TIME_OUT)
    	{
    		return -1;
    	}
    }
    return _serial.read() - '0';
}
void Simulator::addCar(PositionEnum start_pos, PositionEnum final_pos)
{
	_serial.write(Simulator::NEW);
    _serial.write(Simulator::CAR);
    _serial.write(start_pos);
    _serial.write(final_pos);
    _serial.println();
    _sending_start_time = millis();
}
int Simulator::getNumberOfCivilianInLane(PositionEnum pos)
{
    _serial.write(Simulator::GET);
    _serial.write(Simulator::CIVILIAN);
    _serial.write(pos);
    _serial.println();
    _sending_start_time = millis();
    while(!_serial.available())
    {
        if(millis() - _sending_start_time >= TIME_OUT)
        {
            return -1;
        }
    }
    return _serial.read() - '0';
}
int Simulator::getNumberOfCivilianInLane(PositionEnum pos, PositionEnum lane)
{
	_serial.write(Simulator::GET);
    _serial.write(Simulator::CIVILIAN);
    _serial.write(pos);
    _serial.write(lane);
    _serial.println();
    _sending_start_time = millis();
    while(!_serial.available())
    {
        if(millis() - _sending_start_time >= TIME_OUT)
        {
            return -1;
        }
    }
    return _serial.read() - '0';
}
void Simulator::addCivilian()
{
	_serial.write(NEW);
    _serial.write(CIVILIAN);
    _serial.println();
    _sending_start_time = millis();
}
