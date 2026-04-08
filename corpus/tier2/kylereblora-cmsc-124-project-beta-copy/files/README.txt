/*****************************************************************************************
*                                                                                        *
*  Project in Computer Science 124 (Design and Implementation of Programming Languages)  *
*  First Semester School Year 2017-2018                                                  *
*                                                                                        *
*  LOLCODE Interpreter                                                                   *
*  Project Version - Beta Version (Status: Finished)                                   *
*                                                                                        *
*  Developers: Ping Pong Pang                                                            *
*    Andric Quinn S. Baticos                                                             *
*    Kyle Matthew B. Reblora                                                             *
*    Nicolo Jireh D. Unson (Quality Assurance / Quality Control)                         *
*                                                                                        *
*  (c) ALL RIGHTS RESERVED 2017                                                          *
*                                                                                        *
*****************************************************************************************/

	ERROR LIBRARY

		Error 3XXX - Lexical Analyzer Error
			Most of these errors are encountered during parsing.

		Error 8XXX - Syntax Analyzer Error
			These types of errors can be found during the syntax analysis process.

			Error 8000	-	Invalid Use of Keywords
			Error 8100	-	Missing Statements / Arguments
			Error 8200	-	Invalid Arguments
			Error 8500	-	Operation Errors (Arithmetic)

		Error 6XXX - Semantic Analyzer Error
			These types of errors can be found during the semantic analysis process.

			Error 6100	-	Arithmetic Operation Error


	Table 1.1 (Error Table)
	*==========================================================================================*
	| CODE | TYPE | DESCRIPTION                                                                |
	|==========================================================================================|
	| 3000 | LXCL | user input does not match any of the patterns.                             | 
	============================================================================================
	| 8000 | SYNX | invalid re-initialization of main statement                                |
	| 8001 | SYNX | invalid termination of program                                             | 
	| 8003 | SYNX | statements found before HAI delimiter                                      | 
	| 8004 | SYNX | statements found after KTHXBYE delimiter                                   |
	| 8005 | SYNX | duplicate HAI statement                                                    |
	| 8006 | SYNX | invalid declaration of IT statement                                        |
	| 8007 | SYNX | invalid termination of comment                                             |
	| 8008 | SYNX | invalid use of AN statement                                                |
	| 8050 | SYNX | multiple statements in line                                                |
	|------------------------------------------------------------------------------------------|
	| 8100 | SYNX | missing KTHXBYE statement                                                  |
	| 8101 | SYNX | missing HAI statement                                                      |
	| 8102 | SYNX | missing variable identifier for declaration                                |
	| 8103 | SYNX | missing statements after ITZ                                               |
	| 8104 | SYNX | missing variable; variable uninitialized                                   |
	| 8105 | SYNX | missing statements before R operator                                       |
	| 8106 | SYNX | missing statement after R operator                                         |
	| 8107 | SYNX | missing AN statement in binary operator                                    |
	| 8108 | SYNX | missing arguments; arithmetic operation                                    |
	| 8109 | SYNX | missing arguments; gimmeh operation                                        |
	| 8110 | SYNX | missing arguments; boolean operation                                       |
	| 8111 | SYNX | missing AN operation; boolean operation                                    |
	|------------------------------------------------------------------------------------------|
	| 8201 | SYNX | invalid use of variable declaration; variable has been initialized already |
	| 8202 | SYNX | invalid use of variable declaration; ITZ statement not found               |
	| 8203 | SYNX | invalid use of variable declaration; invalid argument                      |
	|------------------------------------------------------------------------------------------|
	| 8300 | SYNX | invalid use of output keyword; statements found before VISIBLE             |
	|------------------------------------------------------------------------------------------|
	| 8500 | SYNX | arithmetic operation; invalid arguments                                    |
	|------------------------------------------------------------------------------------------|
	| 8600 | SYNX | invalid start of SMOOSH function                                           |
	| 8601 | SYNX | expected values after SMOOSH                                               |
	| 8602 | SYNX | invalid value for SMOOSH                                                   |
	|------------------------------------------------------------------------------------------|
	| 8700 | SYNX | boolean operation; invalid arguments                                       |
	| 8701 | SYNX | boolean operation; missing MKAY statement                                  |
	============================================================================================
	| 6000 | SMNC | invalid operation of data types                                            |
	*==========================================================================================*
