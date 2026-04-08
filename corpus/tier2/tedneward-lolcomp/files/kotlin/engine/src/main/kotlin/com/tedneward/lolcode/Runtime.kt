package com.tedneward.lolcode

import kotlin.text.*

class Variant(v : Any? = null) {
    companion object Utility {
        fun isBoolean(value : String) : Boolean {
            return try { value.lowercase().toBooleanStrict(); true; } catch (e : Exception) { false }
        }
        fun isLong(value : String) : Boolean {
            return try { value.toLong(); true; } catch (e : Exception) { false }
        }
        fun isDouble(value : String) : Boolean {
            return try { value.toDouble(); true; } catch (e : Exception) { false }
        }
    }

    enum class TYPE { 
        // NULL
        NOOB {
            override fun toString(value : Any) : String { return "[NOOB]" }
            override fun asBoolean(value : Any) : Boolean { return false }
            override fun asInt64(value : Any) : Long { throw Exception("CANT CONVER NOOB") }
            override fun asDouble(value : Any) : Double { throw Exception("CANT CONVER NOOB") }
            override fun asString(value : Any) : String { throw Exception("CANT CONVER NOOB") }
        },
        // Boolean
        TROOF {
            override fun toString(value : Any) : String { return "[${value} (TROOF)]" }
            override fun asBoolean(value : Any) : Boolean { return if (value as Boolean) true else false }
            override fun asInt64(value : Any) : Long { return if (value as Boolean) 1L else 0L }
            override fun asDouble(value : Any) : Double { return if (value as Boolean) 1.0 else 0.0 }
            override fun asString(value : Any) : String { return if (value as Boolean) "WIN" else "FAIL" }
        },
        // Int64
        NUMBR {
            override fun toString(value : Any) : String { return "[${value } (NUMBR)]" }
            override fun asBoolean(value : Any) : Boolean { return (value.toString().toLong() != 0L) }
            override fun asInt64(value : Any) : Long { return value.toString().toLong() }
            override fun asDouble(value : Any) : Double { return value.toString().toDouble() }
            override fun asString(value : Any) : String { return value.toString() }
        },
        // Double
        NUMBAR {
            override fun toString(value : Any) : String { return "[${value} (NUMBAR)]" }
            override fun asBoolean(value : Any) : Boolean { return if (value == 0.0) false else true }
            override fun asInt64(value : Any) : Long { return (value as Double).toLong() }
            override fun asDouble(value : Any) : Double { return value.toString().toDouble() }
            override fun asString(value : Any) : String { return value.toString() }
        },
        // String
        YARN {
            override fun toString(value : Any) : String { return "[${value} (YARN)]" }
            override fun asBoolean(value : Any) : Boolean { return if (value != "") true else false }
            override fun asInt64(value : Any) : Long { return try { value.toString().toLong() } catch (e: Exception) { throw Exception("CANT CONVER YARN") } }
            override fun asDouble(value : Any) : Double { return try { value.toString().toDouble() } catch (e: Exception) { throw Exception("CANT CONVER YARN") } }
            override fun asString(value : Any) : String { return value.toString() }
        };
        // Array
        //BUKKIT

        abstract fun toString(value : Any) : String

        abstract fun asBoolean(value : Any) : Boolean 
        abstract fun asInt64(value : Any) : Long 
        abstract fun asDouble(value : Any) : Double 
        abstract fun asString(value : Any) : String
    }

    public val value : Any
    public val type : TYPE
    init {
        // We should try to interpret value's type here
        val (ty,va) = when (v) {
            null -> Pair(TYPE.NOOB, "")
            is Boolean -> Pair(TYPE.TROOF, v.toString().toBoolean())
            is Int -> Pair(TYPE.NUMBR, v.toLong())
            is Long -> Pair(TYPE.NUMBR, v)
            is Float -> Pair(TYPE.NUMBAR, v.toDouble())
            is Double -> Pair(TYPE.NUMBAR, v)
            is String -> {
                if (Variant.isLong(v))
                    Pair(TYPE.NUMBR, v.toString().toLong())
                else if (Variant.isDouble(v))
                    Pair(TYPE.NUMBAR, v.toString().toDouble())
                else if (Variant.isBoolean(v))
                    Pair(TYPE.TROOF, v.toString().toBoolean())
                else if (v == "NOOB")
                    Pair(TYPE.NOOB, "")
                else if (v == "WIN")
                    Pair(TYPE.TROOF, true)
                else if (v == "FAIL")
                    Pair(TYPE.TROOF, false)
                else
                    Pair(TYPE.YARN, v.toString())
            }
            is Variant -> Pair(TYPE.YARN, v.asString())
            else -> Pair(TYPE.YARN, v.toString()) // Assume it's a String if nothing else works
        }
        type = ty
        value = va
    }    

    public override fun toString() : String { return type.toString(value) }

    fun asBoolean() : Boolean { return type.asBoolean(value) }
    fun asInt64() : Long { return type.asInt64(value) }
    fun asDouble() : Double { return type.asDouble(value) }
    fun asString() : String { return type.asString(value) }

    fun isTroof() : Boolean { return type == TYPE.TROOF }
    fun isNumbr() : Boolean { return type == TYPE.NUMBR }
    fun isNumbar() : Boolean { return type == TYPE.NUMBAR }
    fun isYarn() : Boolean { return type == TYPE.YARN }

    fun canConvertNumbr() : Boolean { 
        return try { asInt64(); true } catch (e: Exception) { false }
    }
    fun canConvertNumbar() : Boolean { 
        return try { asDouble(); true } catch (e: Exception) { false }
    }

    public override fun equals(other : Any?) : Boolean {
        // Check for comparison to self
        if (this === other)
            return true

        // Make sure it's a Variant
        if (other is Variant) {
            if (canConvertNumbar() && other.canConvertNumbar()) {
                return this.asDouble() == other.asDouble()
            }

            // Can we convert to int?
            if (canConvertNumbr() && other.canConvertNumbr()) {
                return this.asInt64() == other.asInt64()
            }

            // Fine, string-lexical ordinal comparison
            return this.asString().compareTo(other.asString()) == 0
        }

        return false
    }

    public fun greaterThan(other : Variant) : Boolean {
        // Can we convert to double?
        if (canConvertNumbar() && other.canConvertNumbar()) {
            return this.asDouble() > other.asDouble()
        }

        // Can we convert to int?
        if (canConvertNumbr() && other.canConvertNumbr()) {
            return this.asInt64() > other.asInt64()
        }

        // Fine, string-lexical ordinal comparison
        return this.asString().compareTo(other.asString()) > 0
    }
    public fun lesserThan(other : Variant) : Boolean {
        // Can we convert to double?
        if (canConvertNumbar() && other.canConvertNumbar()) {
            return this.asDouble() < other.asDouble()
        }

        // Can we convert to int?
        if (canConvertNumbr() && other.canConvertNumbr()) {
            return this.asInt64() < other.asInt64()
        }

        // Fine, string-lexical ordinal comparison
        return this.asString().compareTo(other.asString()) < 0
    }
    public fun not() : Variant {
        if (isTroof())
            return Variant(! this.asBoolean())
        else if (isNumbar())
            return Variant(- this.asDouble())
        else if (isNumbr())
            return Variant(- this.asInt64())
        else
            return Variant("NOT " + this.asString())
    }
}
