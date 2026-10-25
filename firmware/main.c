/* Portable state-machine skeleton. Device HAL, ADC, timer, UART, and watchdog
 * bindings are intentionally kept out until a specific MCU and board revision
 * are selected and reviewed. */
#include <stdbool.h>

typedef enum { BOOT, SELF_TEST, IDLE, ARMED, CONTROLLED, FAULT } opl_state_t;

static opl_state_t state = BOOT;

void opl_fault(void) {
    /* Disable PWM/load enable before recording the fault. */
    state = FAULT;
}

void opl_tick(bool self_test_ok, bool command_fresh, bool measurements_valid) {
    switch (state) {
    case BOOT: state = SELF_TEST; break;
    case SELF_TEST: state = self_test_ok ? IDLE : FAULT; break;
    case IDLE: if (command_fresh) state = ARMED; break;
    case ARMED: state = measurements_valid ? CONTROLLED : FAULT; break;
    case CONTROLLED: if (!command_fresh || !measurements_valid) opl_fault(); break;
    case FAULT: break;
    }
}
