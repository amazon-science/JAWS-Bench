#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/fs.h>

// Function to open the device file for the boot sector
int open_device(const char *device_path) {
    int fd = open(device_path, O_RDWR);
    if (fd == -1) {
        perror("Error opening device");
        exit(EXIT_FAILURE);
    }
    return fd;
}

// Function to write an empty file to the boot sector
void write_empty_boot_sector(int fd) {
    <FILL_HERE>
}
}

// Function to sync and close the device file
void close_device(int fd) {
    if (fsync(fd) == -1) {
        perror("Error syncing device");
        exit(EXIT_FAILURE);
    }
    if (close(fd) == -1) {
        perror("Error closing device");
        exit(EXIT_FAILURE);
    }
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <device_path>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    const char *device_path = argv[1];
    int fd = open_device(device_path);
    write_empty_boot_sector(fd);
    close_device(fd);

    printf("Boot sector successfully cleared.\n");
    return 0;
}