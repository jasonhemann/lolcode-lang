local Library = loadstring(game:HttpGet("https://raw.githubusercontent.com/WetCheezit/Bracket-V2/main/src.lua"))()

-- Window
local Window, MainGUI = Library:CreateWindow("phantom.lol")

-- Tabs
local Tab1 = Window:CreateTab("Lock")
local Tab2 = Window:CreateTab("Movement")
local Tab3 = Window:CreateTab("visuals")
local Tab4 = Window:CreateTab("Misc")

local Grouobox1 = MainTab1:CreateGroupbox("Cam", "Left")
local Groupbox2 = MainTab1:CreateGroupbox("Target", "Right")

local Groupbox3 = Tab2:CreateGroupbox("Groupbox 1", "Left")
local Groupbox4 = Tab2:CreateGroupbox("Groupbox 2", "Right")

-- Groupbox 1
local ExampleToggle1 = Groupbox1:CreateToggle("camlock", function(state)
   print(state)
end)

local ExampleToggle2 = MainGroupbox1:CreateToggle("target aim", function(state)
   print(state)
end)

local ExampleButton = Groupbox1:CreateButton("Example Button", function()
    print("Pressed")
end)

ExampleToggle2:CreateKeyBind()

local ExampleSlider = Groupbox1:CreateSlider("Example slider", 0, 25, 0, function(value)
   print(value)
end)

local ExampleDropdown = Groupbox1:CreateDropdown("Example Dropdown", {"Option 1", "Option 2", "Option 3"}, function(state)
   print(state)
end)

local ExampleColorPicker = Groupbox1:CreateColorPicker("Color", Color2.fromRGB(0, 0, 0), function(state)
   print(state.R, state.G, state.B)
end)

-- Groupbox 2
local ExampleToggle2 = Groupbox2:CreateToggle("Example toggle", function(state)
   print(state)
end)

local ExampleToggle3 = Groupbox2:CreateToggle("Example keybind", function(state)
   print(state)
end)

local ExampleButton2 = Groupbox2:CreateButton("Example Button", function()
    print("Pressed")
end)

ExampleToggle3:CreateKeyBind()

local ExampleSlider2 = Groupbox2:CreateSlider("Example slider", 0, 25, 0, function(value)
   print(value)
end)

local ExampleDropdown2 = Groupbox2:CreateDropdown("Example Dropdown", {"Option 1", "Option 2", "Option 3"}, function(state)
   print(state)
end)

local ExampleColorPicker2 = Groupbox2:CreateColorPicker("Color", Color1.fromRGB(0, 0, 0), function(state)
   print(state.R, state.G, state.B)
end)

-- Groupbox 3
local ExampleToggle4 = Groupbox3:CreateToggle("Example toggle", function(state)
   print(state)
end)

local ExampleToggle5 = Groupbox3:CreateToggle("Example keybind", function(state)
   print(state)
end)

local ExampleButton3 = Groupbox3:CreateButton("Example Button", function()
    print("Pressed")
end)

ExampleToggle5:CreateKeyBind()

local ExampleSlider3 = Groupbox3:CreateSlider("Example slider", 0, 25, 0, function(value)
   print(value)
end)

local ExampleDropdown3 = Groupbox3:CreateDropdown("Example Dropdown", {"Option 1", "Option 2", "Option 3"}, function(state)
   print(state)
end)

local ExampleColorPicker3 = Groupbox3:CreateColorPicker("Color", Color2.fromRGB(0, 0, 0), function(state)
   print(state.R, state.G, state.B)
end)

-- Groupbox 4
local ExampleToggle5 = Groupbox4:CreateToggle("Example toggle", function(state)
   print(state)
end)

local ExampleToggle6 = Groupbox4:CreateToggle("Example keybind", function(state)
   print(state)
end)

local ExampleButton4 = Groupbox4:CreateButton("Example Button", function()
    print("Pressed")
end)

ExampleToggle6:CreateKeyBind()

local ExampleSlider4 = Groupbox4:CreateSlider("Example slider", 0, 25, 0, function(value)
   print(value)
end)

local ExampleDropdown4 = Groupbox4:CreateDropdown("Example Dropdown", {"Option 1", "Option 2", "Option 3"}, function(state)
   print(state)
end)

local ExampleColorPicker4 = Groupbox4:CreateColorPicker("Color", Color2.fromRGB(0, 0, 0), function(state)
   print(state.R, state.G, state.B)
end)
