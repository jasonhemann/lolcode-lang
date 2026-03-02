(
  #hasheq(
    (id . "v1_2_declare_assign")
    (spec-version . "1.3")
    (title . "Declaration and assignment")
    (source-file . "programs/v1_2_declare_assign.lol")
    (expected-stdout . #f)
    (source-ref . "v1.2:109-113")
    (tags . ("variables" "assignment")))

  #hasheq(
    (id . "v1_2_orly_inline")
    (spec-version . "1.3")
    (title . "Inline O RLY example")
    (source-file . "programs/v1_2_orly_inline.lol")
    (expected-stdout . "J00 HAV A CAT\n")
    (source-ref . "v1.2:354-358")
    (tags . ("control-flow" "orly")))

  #hasheq(
    (id . "v1_2_orly_mebbe")
    (spec-version . "1.3")
    (title . "O RLY with MEBBE branch")
    (source-file . "programs/v1_2_orly_mebbe.lol")
    (expected-stdout . "NOM NOM NOM. I EATED IT.\n")
    (source-ref . "v1.2:380-385")
    (tags . ("control-flow" "orly" "mebbe")))

  #hasheq(
    (id . "v1_2_wtf_case")
    (spec-version . "1.3")
    (title . "WTF case/fallthrough example")
    (source-file . "programs/v1_2_wtf_case.lol")
    (expected-stdout . "FISH HAS A FLAVOR\n")
    (source-ref . "v1.2:406-418")
    (tags . ("control-flow" "wtf")))

  #hasheq(
    (id . "v1_3_typed_declaration")
    (spec-version . "1.3")
    (title . "Typed declaration default value")
    (source-file . "programs/v1_3_typed_declaration.lol")
    (expected-stdout . "0\n")
    (source-ref . "v1.3:126-137")
    (tags . ("variables" "types")))

  #hasheq(
    (id . "v1_3_srs_identifier")
    (spec-version . "1.3")
    (title . "SRS identifier cast in declaration")
    (source-file . "programs/v1_3_srs_identifier.lol")
    (expected-stdout . "0\n")
    (source-ref . "v1.3:185-193")
    (tags . ("variables" "srs")))

  #hasheq(
    (id . "v1_3_bukkit_slots")
    (spec-version . "1.3")
    (title . "BUKKIT declaration and slot assignment")
    (source-file . "programs/v1_3_bukkit_slots.lol")
    (expected-stdout . "42\n")
    (source-ref . "v1.3:619-633,731-733")
    (tags . ("bukkit" "slots")))

  #hasheq(
    (id . "v1_3_function_call")
    (spec-version . "1.3")
    (title . "Function definition, return, and call")
    (source-file . "programs/v1_3_function_call.lol")
    (expected-stdout . "5\n")
    (source-ref . "v1.3:574-600")
    (tags . ("functions" "return")))

  #hasheq(
    (id . "v1_3_object_alt_syntax")
    (spec-version . "1.3")
    (title . "O HAI IM alternate object syntax")
    (source-file . "programs/v1_3_object_alt_syntax.lol")
    (expected-stdout . "pikachu\n")
    (source-ref . "v1.3:716-723,731-733")
    (tags . ("bukkit" "objects")))

  #hasheq(
    (id . "v1_2_loop_uppin_til")
    (spec-version . "1.3")
    (title . "IM IN YR loop with UPPIN and TIL")
    (source-file . "programs/v1_2_loop_uppin_til.lol")
    (expected-stdout . "10\n")
    (source-ref . "v1.2:loop-construct")
    (tags . ("control-flow" "loop")))

  #hasheq(
    (id . "v1_2_logic_variadics")
    (spec-version . "1.3")
    (title . "NOT, ALL OF, and ANY OF operators")
    (source-file . "programs/v1_2_logic_variadics.lol")
    (expected-stdout . "WIN\nWIN\n")
    (source-ref . "v1.2:logic-operators")
    (tags . ("operators" "logic")))

  #hasheq(
    (id . "v1_2_literals_comments")
    (spec-version . "1.3")
    (title . "WIN/FAIL/NOOB literals and OBTW comments")
    (source-file . "programs/v1_2_literals_comments.lol")
    (expected-stdout . "WIN\nNOOB\n")
    (source-ref . "v1.2:literals-comments")
    (tags . ("literals" "comments")))

  #hasheq(
    (id . "v1_2_line_continuation")
    (spec-version . "1.3")
    (title . "Line continuation with ellipsis")
    (source-file . "programs/v1_2_line_continuation.lol")
    (expected-stdout . "AB\n")
    (source-ref . "v1.2:line-continuation")
    (tags . ("syntax" "continuation")))

  #hasheq(
    (id . "v1_2_nested_loops")
    (spec-version . "1.3")
    (title . "Nested IM IN YR loops")
    (source-file . "programs/v1_2_nested_loops.lol")
    (expected-stdout . "6\n")
    (source-ref . "v1.2:loop-nesting")
    (tags . ("control-flow" "loop")))

  #hasheq(
    (id . "v1_3_slot_cast")
    (spec-version . "1.3")
    (title . "IS NOW A cast on BUKKIT slot")
    (source-file . "programs/v1_3_slot_cast.lol")
    (expected-stdout . "42\n")
    (source-ref . "v1.3:casting-slots")
    (tags . ("bukkit" "types" "cast")))

  #hasheq(
    (id . "v1_3_object_method_call")
    (spec-version . "1.3")
    (title . "Object method definition and call")
    (source-file . "programs/v1_3_object_method_call.lol")
    (expected-stdout . "3\n6\n6\n")
    (source-ref . "v1.3:object-method-call")
    (tags . ("bukkit" "objects" "functions")))
)
