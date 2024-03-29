#ifndef _ERROR_H
#define _ERROR_H

enum {
	ERR_TEST						= 0x0001,

// enkel.c
	ERROR_UNRECOGNIZED_SYMBOL				= 0x0401,
	ERROR_ARRINDEX_UNKNOWN_INDEX_TYPE			= 0x0402,
	ERROR_SYNTAX_ERROR					= 0x0403,
	ERROR_TERM_INVALID_OPERATOR				= 0x0404,
	ERROR_EXPRESSION_INVALID_OPERATOR			= 0x0405,
	ERROR_CONDITION_RELATIONAL_INVALID_OPERATOR		= 0x0406,
	ERROR_INPUT_OPTIONS					= 0x0407,
	ERROR_FILE_OPTIONS					= 0x0408,

// scan.c
	ERROR_EXCEEDED_BUFFER_LENGTH				= 0x0501,
	ERROR_COMPARATION_OR_SHIFT_SYMBOL			= 0x0502,
	ERROR_TOKEN_NOT_IDENTIFIED				= 0x0503,

	ERROR_PREVIOUS_DECLARATION_PARAMETER			= 0x0601,
	ERROR_PREVIOUS_DECLARATION_CONSTANT			= 0x0602,
	ERROR_PREVIOUS_DECLARATION_ARRAY			= 0x0603,
	ERROR_PREVIOUS_DECLARATION_GLOBAL_VARIABLE		= 0x0604,
	ERROR_PREVIOUS_DECLARATION_LOCAL_VARIABLE		= 0x0605,

// symbol.c
	ERROR_PREVIOUS_DECLARATION_GLOBAL_IDENT			= 0x0701,
	ERROR_NO_PREVIOUS_DECLARATION_GLOBAL_IDENT		= 0x0702,
	ERROR_PREVIOUS_DECLARATION_LOCAL_IDENT_LEVEL		= 0x0703,
	ERROR_NO_PREVIOUS_DECLARATION_LOCAL_IDENT_LEVEL		= 0x0704

} ERROR;

extern void errnum(int error);
extern int printsymbol(int s);

#endif
