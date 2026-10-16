#ifndef CHIP8_CHIP8STATE_H
#define CHIP8_CHIP8STATE_H

#define CHIP8_SCREEN_WIDTH 64
#define CHIP8_SCREEN_HEIGHT 32

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

typedef struct {
  uint8_t *memory;
  uint8_t *v;
  uint16_t *stack;
  bool *keyboard;
  bool *screen;
  uint8_t *keyboard_time_left;
  uint16_t I;
  uint8_t sound_timer;
  uint8_t delay_timer;
  uint16_t pc;
  uint8_t sp;
  bool waiting_for_key_press;
  size_t register_to_save_key;
} chip8_state_t;

void chip8_state_init(chip8_state_t *state);

void chip8_state_free(chip8_state_t *state);

void chip8_load_cartridge(chip8_state_t *state, FILE *cart);

void chip8_decrement_keyboard_timeout(chip8_state_t *state);

#endif /* CHIP8_CHIP8STATE_H */