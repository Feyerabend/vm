#include "Chip8State.h"
#include "decoder.h"
#include "string.h"
#include <ncurses.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define OVERCLOCK_FACTOR 0.12
#define NANOS_BETWEEN_CYCLES (16666666 * OVERCLOCK_FACTOR)
#define KEYBOARD_TIMEOUT_CYCLES 50

#define map_key(physical, virtual)                                             \
  case physical:                                                               \
    state->keyboard_time_left[virtual] = KEYBOARD_TIMEOUT_CYCLES;              \
    if (state->waiting_for_key_press) {                                        \
      state->v[state->register_to_save_key] = virtual;                         \
    }                                                                          \
    break;

void get_keyboard_input(chip8_state_t *state) {

  char input = getch(); // ncurses

  switch (input) {
    map_key('1', 0x1);
    map_key('2', 0x2);
    map_key('3', 0x3);
    map_key('4', 0xC);
    map_key('q', 0x4);
    map_key('w', 0x5);
    map_key('e', 0x6);
    map_key('r', 0xD);
    map_key('a', 0x7);
    map_key('s', 0x8);
    map_key('d', 0x9);
    map_key('f', 0xE);
    map_key('z', 0xA);
    map_key('x', 0x0);
    map_key('c', 0xB);
    map_key('v', 0xF);

  default:
    break;
  }
  if (state->waiting_for_key_press && input != ERR) {
    state->pc = state->pc + 2;
    state->waiting_for_key_press = false;
  }

  for (size_t i = 0; i < 16; i++) {
    state->keyboard[i] = state->keyboard_time_left[i] > 0;
  }
}

int main(int argc, char **argv) {
  srand(time(NULL));
  // open the cartridge file
  FILE *cart;
  if (argc >= 2) {
    cart = fopen(argv[1], "rb");
  } else {
    printf("usage Chip8 PATH_TO_GAME\n");
    return -1;
  }

  // create and initialize the chip8 vm state and close the file
  chip8_state_t state;
  chip8_state_init(&state);
  chip8_load_cartridge(&state, cart);
  fclose(cart);

  struct timespec time_since_last_cycle;
  clock_gettime(CLOCK_MONOTONIC, &time_since_last_cycle);

  if (!DEBUG) { // ncurses
    initscr();
    noecho();
    cbreak();
    nodelay(stdscr, true);
  }

  while (true) {
    uint16_t opcode = decoder_get_current_opcode(&state);
    instruction_t instruction = decoder_opcode_to_instruction(opcode);
    decoder_execute_instruction(&state, instruction);
    chip8_decrement_keyboard_timeout(&state);

    if (!DEBUG) {
      // draw the screen
      for (size_t row = 0; row < CHIP8_SCREEN_HEIGHT; row++) {
        for (size_t col = 0; col < CHIP8_SCREEN_WIDTH; col++) {
          size_t screen_index = row * CHIP8_SCREEN_WIDTH + col;
          mvaddch(row, col, state.screen[screen_index] ? '#' : ' '); // ncurses
        }
      }

      if (state.sound_timer > 0) {
        beep();
      }

      get_keyboard_input(&state);
      refresh();
    }

    // slow loop down to 60HZ
    struct timespec current_time;
    clock_gettime(CLOCK_MONOTONIC, &current_time);
    while (current_time.tv_nsec - time_since_last_cycle.tv_nsec <
           NANOS_BETWEEN_CYCLES) {
      if (!DEBUG) {
        get_keyboard_input(&state);
      }
      clock_gettime(CLOCK_MONOTONIC, &current_time);
      if (current_time.tv_nsec - time_since_last_cycle.tv_nsec < 0) {
        break;
      }
    }
    clock_gettime(CLOCK_MONOTONIC, &time_since_last_cycle);
  }
  return 0;
}