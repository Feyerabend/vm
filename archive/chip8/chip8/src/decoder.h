#ifndef CHIP8_DECODER_H
#define CHIP8_DECODER_H

#define DEBUG 0
#include "Chip8State.h"
#include <stdint.h>

typedef struct {
  uint16_t full_opcode;
  uint8_t I;
  uint8_t X;
  uint8_t Y;
  uint8_t J;
  uint16_t NNN;
  uint8_t KK;
} instruction_t;

uint16_t decoder_get_current_opcode(chip8_state_t *state);

instruction_t decoder_opcode_to_instruction(uint16_t opcode);

void decoder_execute_instruction(chip8_state_t *state,
                                 instruction_t instruction);

#endif