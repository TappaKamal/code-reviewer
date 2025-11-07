; ----------------------------------------------------------
; Tree-sitter Query File for Python
; ----------------------------------------------------------
; These queries help locate key code patterns for static and
; security analysis. You can extend this file to detect more
; complex structures or anti-patterns later.
; ----------------------------------------------------------

; --- Function definitions ---
(
  function_definition
    name: (identifier) @function.name
    parameters: (parameters) @function.params
) @function.definition

; --- Class definitions ---
(
  class_definition
    name: (identifier) @class.name
) @class.definition

; --- Bare except (bad practice) ---
(
  except_clause
    name: (identifier)? @except.name
) @except.clause

; --- Import statements ---
(
  import_statement
    name: (dotted_name) @import.name
) @import.statement

; --- From import statements ---
(
  import_from_statement
    module_name: (dotted_name) @import.module
) @importfrom.statement

; --- Function calls (used by taint and complexity checks) ---
(
  call
    function: (identifier) @call.name
) @call.expression
