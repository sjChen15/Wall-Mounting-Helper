import time
import spidev
import adafruit_adxl34x

# initiaize SPI connection
spi_bus = 0
spi_device = 0
spi = spidev.SpiDev()
spi.open(spi_bus, spi_device)
spi.max_speed_hz = 1000000

# initialize accelerometer
accelerometer = adafruit_adxl34x.ADXL345()

try:
	while True:
		print("%f %f %f"%accelerometer.acceleration)
		time.sleep(1)
except KeyboardInterrupt:
	spi.close()
	quit()
