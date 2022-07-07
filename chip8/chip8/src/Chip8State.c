#include "Chip8State.h"
#include <inttypes.h>
#include <stdlib.h>

void chip8_state_init(chip8_state_t *state) {
  state->memory = calloc(4096, sizeof(uint8_t));
  state->v = calloc(16, sizeof(uint8_t));
  state->stack = calloc(16, sizeof(uint16_t));
  state->keyboard = calloc(16, sizeof(bool));
  state->keyboard_time_left = calloc(16, sizeof(uint8_t));
  state->screen =
      calloc(CHIP8_SCREEN_HEIGHT * CHIP8_SCREEN_WIDTH, sizeof(bool));
  state->I = 0;
  state->sound_timer = 0;
  state->delay_timer = 0;
  state->pc = 0x200;
  state->sp = 0;
  state->waiting_for_key_press = false;
  state->register_to_save_key = 0;

  const uint8_t fontset[0x10 * 5] = {
      0xF0, 0x90, 0x90, 0x90, 0xF0, // 0
      0x20, 0x60, 0x20, 0x20, 0x70, // 1
      0xF0, 0x10, 0xF0, 0x80, 0xF0, // 2
      0xF0, 0x10, 0xF0, 0x10, 0xF0, // 3
      0x90, 0x90, 0xF0, 0x10, 0x10, // 4
      0xF0, 0x80, 0xF0, 0x10, 0xF0, // 5
      0xF0, 0x80, 0xF0, 0x90, 0xF0, // 6
      0xF0, 0x10, 0x20, 0x40, 0x40, // 7
      0xF0, 0x90, 0xF0, 0x90, 0xF0, // 8
      0xF0, 0x90, 0xF0, 0x10, 0xF0, // 9
      0xF0, 0x90, 0xF0, 0x90, 0x90, // A
      0xE0, 0x90, 0xE0, 0x90, 0xE0, // B
      0xF0, 0x80, 0x80, 0x80, 0xF0, // C
      0xE0, 0x90, 0x90, 0x90, 0xE0, // D
      0xF0, 0x80, 0xF0, 0x80, 0xF0, // E
      0xF0, 0x80, 0xF0, 0x80, 0x80  // F
  };

  for (size_t offset = 0; offset < 0x10 * 5; offset++) {
    state->memory[offset] = fontset[offset];
  }
}

void chip8_state_free(chip8_state_t *state) {
  free(state->memory);
  free(state->v);
  free(state->stack);
  free(state->keyboard);
  free(state->screen);
  free(state->keyboard_time_left);
}

void chip8_load_cartridge(chip8_state_t *state, FILE *cart) {
  fseek(cart, 0, SEEK_END);
  size_t file_length = ftell(cart);
  rewind(cart);

  fread(state->memory + 0x200, file_length, 1, cart);
}

void chip8_decrement_keyboard_timeout(chip8_state_t *state) {
  for (size_t i = 0; i < 16; i++) {
    if (state->keyboard_time_left[i] > 0)
      state->keyboard_time_left[i]--;
  }
}