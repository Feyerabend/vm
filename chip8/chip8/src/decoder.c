#include "decoder.h"
#include "string.h"
#include <stdio.h>
#include <stdlib.h>

#define debug_printf(fmt, ...)                                                 \
  do {                                                                         \
    if (DEBUG)                                                                 \
      printf(fmt, __VA_ARGS__);                                                \
  } while (0)

uint16_t decoder_get_current_opcode(chip8_state_t *state) {
  uint16_t current_pc = state->pc;
  uint16_t msb = state->memory[current_pc];
  uint8_t lsb = state->memory[current_pc + 1];
  uint16_t opcode = (msb << 8) | lsb;
  return opcode;
}

instruction_t decoder_opcode_to_instruction(uint16_t opcode) {
  instruction_t instruction;
  instruction.full_opcode = opcode;
  instruction.I = opcode >> (4 * 3);
  instruction.X = (opcode & 0x0F00) >> (4 * 2);
  instruction.Y = (opcode & 0x00F0) >> 4;
  instruction.NNN = opcode & 0x0FFF;
  instruction.KK = opcode & 0x00FF;
  instruction.J = opcode & 0x000F;

  return instruction;
}

void decoder_execute_instruction(chip8_state_t *state,
                                 instruction_t instruction) {
  if (state->delay_timer > 0)
    state->delay_timer--;
  if (state->sound_timer > 0)
    state->sound_timer--;

  debug_printf("%x ", instruction.full_opcode);
  switch (instruction.I) {
  case 0x0:
    switch (instruction.full_opcode) {
    case 0x00E0:

      // debug_printf("clearscr\n");

      memset(state->screen, false,
             sizeof(bool) * CHIP8_SCREEN_HEIGHT * CHIP8_SCREEN_WIDTH);
      state->pc = state->pc + 2;
      break;
    case 0x00EE:
      debug_printf("return to %x\n", state->stack[state->sp]);
      state->pc = state->stack[state->sp];
      state->sp = state->sp - 1;
      state->pc = state->pc + 2;
      break;
    default:
      goto UNIMPL;
    }
    break;
  case 0x1:
    debug_printf("Jump to %x\n", instruction.NNN);
    state->pc = instruction.NNN;
    break;
  case 0x2:
    debug_printf("Call %x\n", instruction.NNN);
    state->sp = state->sp + 1;
    state->stack[state->sp] = state->pc;
    state->pc = instruction.NNN;
    break;
  case 0x3:
    debug_printf("skip if v[%x] == %x\n", instruction.X, instruction.KK);
    if (state->v[instruction.X] == instruction.KK) {
      state->pc = state->pc + 2;
    }
    state->pc = state->pc + 2;
    break;
  case 0x4:
    debug_printf("skip if v[%x] != %x\n", instruction.X, instruction.KK);
    if (state->v[instruction.X] != instruction.KK) {
      state->pc = state->pc + 2;
    }
    state->pc = state->pc + 2;
    break;
  case 0x5:
    if (instruction.J != 0x0)
      goto UNIMPL;
    debug_printf("skip if v[%x] == v[%x]\n", instruction.X, instruction.Y);
    if (state->v[instruction.X] == instruction.Y) {
      state->pc = state->pc + 2;
    }
    state->pc = state->pc + 2;
    break;
  case 0x6:
    debug_printf("set v[%x] = %x\n", instruction.X, instruction.KK);
    state->v[instruction.X] = instruction.KK;
    state->pc = state->pc + 2;
    break;
  case 0x7:
    debug_printf("set v[%x] = v[%x] + %x\n", instruction.X, instruction.X,
                 instruction.KK);
    state->v[instruction.X] = state->v[instruction.X] + instruction.KK;
    state->pc = state->pc + 2;
    break;
  case 0x8:
    switch (instruction.J) {
    case 0x0:
      debug_printf("v[%x] = v[%x]\n", instruction.X, instruction.Y);
      state->v[instruction.X] = state->v[instruction.Y];
      state->pc = state->pc + 2;
      break;
    case 0x1:
      debug_printf("v[%x] = v[%x] or v[%x]\n", instruction.X, instruction.X,
                   instruction.Y);
      state->v[instruction.X] =
          state->v[instruction.X] | state->v[instruction.Y];
      state->pc = state->pc + 2;
      break;
    case 0x2:
      debug_printf("v[%x] = v[%x] and v[%x]\n", instruction.X, instruction.X,
                   instruction.Y);
      state->v[instruction.X] =
          state->v[instruction.X] & state->v[instruction.Y];
      state->pc = state->pc + 2;
      break;
    case 0x3:
      debug_printf("v[%x] = v[%x] xor v[%x]\n", instruction.X, instruction.X,
                   instruction.Y);
      state->v[instruction.X] =
          state->v[instruction.X] ^ state->v[instruction.Y];
      state->pc = state->pc + 2;
      break;
    case 0x4:
      debug_printf("Set V[%x] = V[%x] + V[%x], set VF = carry\n", instruction.X,
                   instruction.X, instruction.Y);
      uint32_t x = state->v[instruction.X];
      uint32_t y = state->v[instruction.Y];
      if (x + y > 255) {
        state->v[0xF] = 0x1;
      } else {
        state->v[0xF] = 0x0;
      }
      state->v[instruction.X] =
          state->v[instruction.X] + state->v[instruction.Y];
      state->pc = state->pc + 2;
      break;
    case 0x5:
      debug_printf("Set V[%x] = V[%x] - V[%x], set VF = NOT borrow\n",
                   instruction.X, instruction.X, instruction.Y);
      if (state->v[instruction.X] > state->v[instruction.Y]) {
        state->v[0xF] = 0x1;
      } else {
        state->v[0xF] = 0x0;
      }
      state->v[instruction.X] =
          state->v[instruction.X] - state->v[instruction.Y];
      state->pc = state->pc + 2;
      break;
    case 0x6:
      debug_printf("Set V[%x] = V[%x] SHR 1\n", instruction.X, instruction.X);
      if ((state->v[instruction.X] & 0b00000001) == 0x1) {
        state->v[0xF] = 0x1;
      } else {
        state->v[0xF] = 0x0;
      }
      state->v[instruction.X] = state->v[instruction.X] >> 1;
      state->pc = state->pc + 2;
      break;
    case 0x7:
      debug_printf("Set V[%x] = V[%x] - V[%x], set VF = NOT borrow.\n",
                   instruction.X, instruction.Y, instruction.X);
      if (state->v[instruction.Y] > state->v[instruction.X]) {
        state->v[0xF] = 0x1;
      } else {
        state->v[0xF] = 0x0;
      }
      state->v[instruction.X] =
          state->v[instruction.Y] - state->v[instruction.X];
      state->pc = state->pc + 2;
      break;
    case 0xE:
      debug_printf("Set V[%x] = V[%x] SHL 1\n", instruction.X, instruction.X);
      if ((state->v[instruction.X] & 0b10000000) != 0) {
        state->v[0xF] = 0x1;
      } else {
        state->v[0xF] = 0x0;
      }
      state->v[instruction.X] = state->v[instruction.X] << 1;
      state->pc = state->pc + 2;
      break;
    default:
      goto UNIMPL;
    }
    break;
  case 0x9:
    if (instruction.J != 0x0)
      goto UNIMPL;
    debug_printf("Skip next instruction if V[%x] != V[%x].\n", instruction.X,
                 instruction.Y);
    if (state->v[instruction.X] != state->v[instruction.Y]) {
      state->pc = state->pc + 2;
    }
    state->pc = state->pc + 2;
    break;
  case 0xA:
    debug_printf("Set I = %x\n", instruction.NNN);
    state->I = instruction.NNN;
    state->pc = state->pc + 2;
    break;
  case 0xB:
    debug_printf("Jump to location %x + V[0].\n", instruction.NNN);
    state->pc = state->pc + state->v[0];
    break;
  case 0xC:
    debug_printf("Set V[%x] = random byte AND kk.\n", instruction.X);
    state->v[instruction.X] = (rand() % 256) & instruction.KK;
    state->pc = state->pc + 2;
    break;
  case 0xD:
    debug_printf(
        "Display %x-byte sprite starting at memory location I at (V[%x], "
        "V[%x]), set VF = collision.\n",
        instruction.J, instruction.X, instruction.Y);
    bool collision = false;

    // x and y wrap around the screen
    size_t x = state->v[instruction.X];
    x = x % CHIP8_SCREEN_WIDTH;

    size_t y = state->v[instruction.Y];
    y = y % CHIP8_SCREEN_HEIGHT;

    for (size_t offset = 0; offset < instruction.J; offset++) {
      uint8_t current_byte = state->memory[state->I + offset];
      debug_printf("drawing %x\n", current_byte);
      for (size_t bit = 0; bit < 8; bit++) {
        if ((current_byte & (1 << (7 - bit))) != 0) {
          size_t screen_offset = (y + offset) * CHIP8_SCREEN_WIDTH + x + bit;
          if (state->screen[screen_offset]) {
            collision = true;
          }
          state->screen[screen_offset] = state->screen[screen_offset] ^ true;
        }
      }
    }
    state->v[0xF] = collision ? 1 : 0;
    state->pc = state->pc + 2;
    break;
  case 0xE:
    switch (instruction.KK) {
    case 0x9E:
      debug_printf(
          "Skip next instruction if key with the value of V[%x] is pressed.\n",
          instruction.X);
      if (state->keyboard[state->v[instruction.X]]) {
        state->pc = state->pc + 2;
      }
      state->pc = state->pc + 2;
      break;
    case 0xA1:
      debug_printf(
          "Skip next instruction if key with the value of V[%x] not is "
          "pressed.\n",
          instruction.X);
      if (!state->keyboard[state->v[instruction.X]]) {
        state->pc = state->pc + 2;
      }
      state->pc = state->pc + 2;
      break;
    default:
      goto UNIMPL;
    }
    break;
  case 0xF:
    switch (instruction.KK) {
    case 0x07:
      debug_printf("Set V[%x] = delay timer value.\n", instruction.X);
      state->v[instruction.X] = state->delay_timer;
      state->pc = state->pc + 2;
      break;
    case 0x0A:
      debug_printf(
          "Wait for a key press, store the value of the key in V[%x].\n",
          instruction.X);
      state->waiting_for_key_press = true;
      state->register_to_save_key = instruction.X;
      break;
    case 0x15:
      debug_printf("Set delay timer = V[%x].\n", instruction.X);
      state->delay_timer = state->v[instruction.X];
      state->pc = state->pc + 2;
      break;
    case 0x18:
      debug_printf("Set sound timer = V[%x]\n", instruction.X);
      state->sound_timer = state->v[instruction.X];
      state->pc = state->pc + 2;
      break;
    case 0x1E:
      debug_printf("Set I = I + V[%x].\n", instruction.X);
      state->I = state->I + state->v[instruction.X];
      state->pc = state->pc + 2;
      break;
    case 0x29:
      debug_printf("Set I = location of sprite for digit V[%x]\n",
                   instruction.X);
      state->I = 5 * state->v[instruction.X];
      state->pc = state->pc + 2;
      break;
    case 0x33:
      debug_printf(
          "Store BCD representation of V[%x] in memory locations I, I+1, "
          "and I+2",
          instruction.X);
      uint8_t n = state->v[instruction.X];
      state->memory[state->I] = n / 100;
      state->memory[state->I + 1] = (n % 100) / 10;
      state->memory[state->I + 2] = n % 10;
      state->pc = state->pc + 2;
      break;
    case 0x55:
      debug_printf(
          "Store registers V0 through V[%x] in memory starting at location I.",
          instruction.X);
      for (size_t offset = 0; offset <= instruction.X; offset++) {
        state->memory[state->I + offset] = state->v[offset];
      }
      state->pc = state->pc + 2;
      break;
    case 0x65:
      debug_printf(
          "Read registers V0 through V[%x] from memory starting at location I.",
          instruction.X);
      for (size_t offset = 0; offset <= instruction.X; offset++) {
        state->v[offset] = state->memory[state->I + offset];
      }
      state->pc = state->pc + 2;
      break;
    default:
      goto UNIMPL;
    }
    break;
  UNIMPL:
  default:
    debug_printf("Unknown opcode %x\n", instruction.full_opcode);
    exit(1);
  }
}