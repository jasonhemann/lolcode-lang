package com.tedneward.lolcode

import java.io.File
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFalse
import kotlin.test.assertNotEquals
import kotlin.test.assertTrue

class RuntimeTests {
    @Test
    fun variantInitializationGetsTypeRight() {
        fun test(str : String) : Triple<Boolean, Boolean, Boolean> {
            return Triple(Variant.isBoolean(str), Variant.isLong(str), Variant.isDouble(str))
        }

        assertEquals(Triple(false, true, true), test("5"))
        assertEquals(Triple(false, false, true), test("5.0"))
        assertEquals(Triple(false, false, true), test("-15.7"))
        assertEquals(Triple(true, false, false), test("true"))
        assertEquals(Triple(true, false, false), test("TRUE"))
        assertEquals(Triple(true, false, false), test("false"))
        assertEquals(Triple(true, false, false), test("FALSE"))
        assertEquals(Triple(false, false, false), test("This is a boring string"))
    }

    @Test
    fun testVariantBasics() {
        val v = Variant(0)
        assertEquals(0L, v.value)
        assertEquals(Variant.TYPE.NUMBR, v.type)

        assertEquals("0", v.asString())
        assertEquals(0L, v.asInt64())
        assertEquals(0.0, v.asDouble())
        assertFalse(v.asBoolean())
        assertEquals("[0 (NUMBR)]", v.toString())

        val v2 = Variant("0")
        assertEquals(0L, v2.value)
        assertEquals(Variant.TYPE.NUMBR, v2.type)

        assertEquals(0L, v2.asInt64())
        assertFalse(v2.asBoolean())
        assertEquals("[0 (NUMBR)]", v2.toString())
    }
    @Test fun testVariantNOOB() {
        val v = Variant()
        assertEquals("[NOOB]", v.toString())

        try { assertFalse(v.asBoolean())  }
        catch (ex : Exception) { assertTrue(false, "We should be able to convert NOOB to false") }

        try { v.asString(); assertTrue(false, "Should never get here") }
        catch (ex : Exception) { assertEquals("CANT CONVER NOOB", ex.message) }

        try { v.asInt64(); assertTrue(false, "Should never get here")  }
        catch (ex : Exception) { assertEquals("CANT CONVER NOOB", ex.message) }

        try { v.asDouble(); assertTrue(false, "Should never get here")  }
        catch (ex : Exception) { assertEquals("CANT CONVER NOOB", ex.message) }
    }
    @Test fun strings() {
        val v1 = Variant("This is a test")
        assertEquals("This is a test", v1.asString())
    }
    @Test fun testBooleanConversions() {
        assertTrue(Variant(1).asBoolean())
        assertFalse(Variant(0).asBoolean())
        assertTrue(Variant(-1).asBoolean())
        assertFalse(Variant(null).asBoolean())
    }
    @Test fun mathsConversionRules() { 
        val fiveString = Variant("5")
        val fiveDecimalString = Variant("5.2")

        assertEquals(5, fiveString.asInt64())
        assertEquals(5.0, fiveString.asDouble())
        assertEquals(5, fiveDecimalString.asInt64()) // truncates
        assertEquals(5.2, fiveDecimalString.asDouble())
    }
    @Test fun mathsTests() {
        val one = Variant("WIN")
        val two = Variant(2)
        val three = Variant("3.0")
        val four = Variant("4")

        assertEquals(Variant(3).asInt64(), one.asInt64() + two.asInt64())
        assertEquals(Variant(4).asInt64(), one.asInt64() + three.asInt64())
        assertEquals(Variant(5).asInt64(), one.asInt64() + four.asInt64())

        assertEquals(Variant(3).asDouble(), one.asDouble() + two.asDouble())
        assertEquals(Variant(4).asDouble(), one.asDouble() + three.asDouble())
        assertEquals(Variant(5).asDouble(), one.asDouble() + four.asDouble())
    }

    @Test fun comparisonTests() {
        val threeI = Variant(3)
        val threeD = Variant(3.0)
        val threeSI = Variant("3")
        val threeSD = Variant("3.0")
        val fiveI = Variant(5)
        val fiveD = Variant(5.0)
        val fiveSI = Variant("5")
        val fiveSD = Variant("5.0")

        // Test equality variations
        assertEquals(threeI, threeI)
        assertEquals(threeD, threeD)
        assertEquals(threeSI, threeSI)
        assertEquals(threeSD, threeSD)

        assertEquals(threeI, threeD)
        assertEquals(threeD, threeI)
        assertEquals(threeSI, threeI)
        assertEquals(threeI, threeSI)
        assertEquals(threeD, threeSD)
        assertEquals(threeSD, threeD)

        // Test inequality
        assertNotEquals(threeI, fiveI)
        assertNotEquals(threeD, fiveD)
        assertNotEquals(threeSI, fiveSI)
        assertNotEquals(threeSD, fiveSD)

        assertNotEquals(threeI, fiveD)
        assertNotEquals(threeD, fiveI)
        assertNotEquals(threeSI, fiveI)
        assertNotEquals(threeI, fiveSI)
        assertNotEquals(threeD, fiveSD)
        assertNotEquals(threeSD, fiveD)

        assertTrue(threeI.lesserThan(fiveI))
        assertTrue(fiveI.greaterThan(threeI))
        assertTrue(threeD.lesserThan(fiveD))
        assertTrue(fiveD.greaterThan(threeD))
        assertTrue(threeSI.lesserThan(fiveSI))
        assertTrue(fiveSI.greaterThan(threeSI))
        assertTrue(threeSD.lesserThan(fiveSD))
        assertTrue(fiveSD.greaterThan(threeSD))

        assertTrue(threeI.lesserThan(fiveSI))
        assertTrue(fiveI.greaterThan(threeSI))
        assertTrue(threeD.lesserThan(fiveSD))
        assertTrue(fiveD.greaterThan(threeSD))
        assertTrue(threeSI.lesserThan(fiveI))
        assertTrue(fiveSI.greaterThan(threeI))
        assertTrue(threeSD.lesserThan(fiveD))
        assertTrue(fiveSD.greaterThan(threeD))
    }

    @Test fun notTests() {
        val boolVar = Variant(true)
        assertTrue(boolVar.asBoolean())
        val notBoolVar = boolVar.not()
        assertFalse(notBoolVar.asBoolean())
        val notNotBoolVar = notBoolVar.not()
        assertTrue(notNotBoolVar.asBoolean())

        val intVar = Variant(12)
        assertEquals(12, intVar.asInt64())
        assertEquals(-12, intVar.not().asInt64())
        assertEquals(12, intVar.not().not().asInt64())

        val dVar = Variant(12.0)
        assertEquals(12.0, dVar.asDouble())
        assertEquals(-12.0, dVar.not().asDouble())
        assertEquals(12.0, dVar.not().not().asDouble())

        val strVar = Variant("WIZZYRD")
        assertEquals("WIZZYRD", strVar.asString())
        assertEquals("NOT WIZZYRD", strVar.not().asString())
        assertEquals("NOT NOT WIZZYRD", strVar.not().not().asString())
    }

    @Test fun newFrameIsEmpty() {
        val frame = Frame()
        assertFalse(frame.peek("non-existent"))
    }
    @Test fun newFrameCanHoldAVar() {
        val frame = Frame()
        frame.put("x", Variant(5))
        assertTrue(frame.peek("x"))
        assertEquals(frame.get("x"), Variant(5))
    }
    @Test fun frameCanBeInitialized() {
        val vars = mapOf("x" to Variant(5), "y" to Variant(12))
        val frame = Frame(vars)
        assertEquals(frame.get("x"), Variant(5))
        assertEquals(frame.get("y"), Variant(12))
    }
    @Test fun framesStack() {
        val frame = Frame(mapOf("x" to Variant(5), "y" to Variant(12)))
        assertEquals(frame.get("x"), Variant(5))
        assertEquals(frame.get("y"), Variant(12))

        val nestedFrame = Frame(mapOf(), frame)
        assertEquals(nestedFrame.get("x"), Variant(5))
        assertEquals(nestedFrame.get("y"), Variant(12))
    }
}
