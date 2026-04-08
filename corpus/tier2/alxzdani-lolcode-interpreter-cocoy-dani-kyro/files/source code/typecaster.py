class TypeCaster:
    # implicitly converts various input types to boolean TROOF (WIN/FAIL)
    @staticmethod
    def implicit_cast_to_troof(value):
        # handle NOOB as FAIL
        if value is None:
            return False

        # handle numeric types
        if isinstance(value, (int, float)):
            return False if value == 0 else True

        # handle string types
        if isinstance(value, str):
            stripped = value.strip()
            if stripped == "" or stripped == "0":
                return False
            elif stripped.lower() == "fail":
                return False
            else:
                return True

        # handle TROOF
        if isinstance(value, bool):
            return True if value else False

        # default to True for other types
        return True

    # implicitly converts input to numeric type (NUMBR or NUMBAR)
    @staticmethod
    def implicit_cast_to_numeric(value):
        # handle NOOB
        if value is None:
            return 0

        # handle TROOF
        if isinstance(value, bool):
            return 1 if value else 0

        # handle string
        if isinstance(value, str):
            clean_value = value.strip()
            try:
                # try integer conversion first
                if clean_value.isdigit() or (clean_value.startswith('-') and clean_value[1:].isdigit()):
                    return int(clean_value)
                # try float conversion
                elif '.' in clean_value:
                    return float(clean_value)
                else:
                    raise ValueError(f"Cannot convert '{clean_value}' to numeric type")
            except ValueError:
                raise ValueError(f"Invalid numeric string: '{clean_value}'")

        # handle existing numeric types
        if isinstance(value, int):
            return value # NUMBR
        if isinstance(value, float):
            return value # NUMBAR

        raise ValueError(f"Cannot cast {type(value).__name__} to numeric type")
    
    # explicitly converts input to numeric type (NUMBR or NUMBAR)
    @staticmethod
    def explicit_cast_to_numeric(value, target_type):
        # handle NOOB
        if value is None:
            return 0 if target_type == 'NUMBR' else 0.0

        # handle TROOF
        if isinstance(value, bool):
            return 1 if value == 'WIN' else 0

        # handle string
        if isinstance(value, str):
            clean_value = value.strip()
            try:
                # try integer conversion first
                if clean_value.isdigit() or (clean_value.startswith('-') and clean_value[1:].isdigit()):
                    return int(clean_value) if target_type == 'NUMBR' else float(clean_value)
                # try float conversion
                elif '.' in clean_value:
                    return float(clean_value)
                else:
                    raise ValueError(f"Cannot convert '{clean_value}' to numeric type")
            except ValueError:
                raise ValueError(f"Invalid numeric string: '{clean_value}'")

        # handle existing numeric types
        if isinstance(value, int):
            return value if target_type == 'NUMBR' else float(value)
        if isinstance(value, float):
            if target_type == 'NUMBR':
                return int(value)
            return value # NUMBAR

        raise ValueError(f"Cannot cast {type(value).__name__} to numeric type")

    # implicitly converts various input types to YARN (string)
    @staticmethod
    def implicit_cast_to_yarn(value):
        # handle NOOB as empty string
        if value is None:
            return ""
        
        # handle TROOF conversion to "WIN" or "FAIL"
        if isinstance(value, bool):
            return "WIN" if value else "FAIL"
        
        # handle NUMBAR truncation to two decimal places
        if isinstance(value, float):
            return f"{value}"
        
        # handle NUMBR conversion to string
        if isinstance(value, int):
            return str(value)
        
        # handle existing string
        if isinstance(value, str):
            return value
        
        # Fallback for other types
        return str(value)

    # performs explicit type casting to specified LOLCode type
    @staticmethod
    def explicit_cast(value, target_type):
        if target_type == 'TROOF':
            return TypeCaster.implicit_cast_to_troof(value)
        elif target_type in ['NUMBAR', 'NUMBR']:
            return TypeCaster.explicit_cast_to_numeric(value, target_type)
        elif target_type == 'YARN':
            return TypeCaster.implicit_cast_to_yarn(value)
        elif target_type == 'NOOB':
            return None
        
        raise ValueError(f"Unsupported target type: {target_type}")

    # determines the LOLCode type of a given value
    @staticmethod
    def type_check(value):
        if value is None:
            return 'NOOB'
        
        if isinstance(value, bool):
            return 'TROOF'
        
        if isinstance(value, int):
            return 'NUMBR'
        
        if isinstance(value, float):
            return 'NUMBAR'
        
        if isinstance(value, str):
            return 'YARN'
        
        raise ValueError(f"Unrecognized type for value: {value}")

    # checks if a value is numeric (NUMBR or NUMBAR)
    @staticmethod
    def is_numeric(value):
        return isinstance(value, (int, float))

    # checks if two values can be directly compared in LOLCode
    @staticmethod
    def can_compare(value1, value2):
        return TypeCaster.is_numeric(value1) and TypeCaster.is_numeric(value2) and type(value1) == type(value2)