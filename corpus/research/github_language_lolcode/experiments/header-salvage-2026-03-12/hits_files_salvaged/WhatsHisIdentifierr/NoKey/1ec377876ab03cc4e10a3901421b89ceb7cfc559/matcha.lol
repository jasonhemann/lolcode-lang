-- leaked by alt_
loadstring(game:HttpGet("https://raw.githubusercontent.com/WhatsHisIdentifierr/NoKey/refs/heads/main/Discord",true))()
repeat wait() until game:IsLoaded()

game:GetService("CorePackages").Packages:Destroy()

assert(getrawmetatable)
grm = getrawmetatable(game)
setreadonly(grm, false)
old = grm.__namecall
grm.__namecall = newcclosure(function(self, ...)
    local args = {...}
    if tostring(args[1]) == "TeleportDetect" then
        return
    elseif tostring(args[1]) == "CHECKER_1" then
        return
    elseif tostring(args[1]) == "CHECKER" then
        return
    elseif tostring(args[1]) == "GUI_CHECK" then
        return
    elseif tostring(args[1]) == "OneMoreTime" then
        return
    elseif tostring(args[1]) == "checkingSPEED" then
        return
    elseif tostring(args[1]) == "BANREMOTE" then
        return
    elseif tostring(args[1]) == "PERMAIDBAN" then
        return
    elseif tostring(args[1]) == "KICKREMOTE" then
        return
    elseif tostring(args[1]) == "BR_KICKPC" then
        return
    elseif tostring(args[1]) == "BR_KICKMOBILE" then
        return
    end
    return old(self, ...)
end)
if not game:IsLoaded() then 
    game.Loaded:Wait()
end

if not syn or not protectgui then
    getgenv().protectgui = function() end
end

task.spawn(function()
	local g = getinfo or debug.getinfo
	local d = false
	local h = {}

	local x, y

	setthreadidentity(2)

	for i, v in getgc(true) do
		if typeof(v) == "table" then
			local a = rawget(v, "Detected")
			local b = rawget(v, "Kill")
		
			if typeof(a) == "function" and not x then
				x = a
				local o; o = hookfunction(x, function(c, f, n)
					if c ~= "_" then
						if d then
						end
					end
					
					return true
				end)
				table.insert(h, x)
			end

			if rawget(v, "Variables") and rawget(v, "Process") and typeof(b) == "function" and not y then
				y = b
				local o; o = hookfunction(y, function(f)
					if d then
					end
				end)
				table.insert(h, y)
			end
		end
	end

	local o; o = hookfunction(getrenv().debug.info, newcclosure(function(...)
		local a, f = ...

		if x and a == x then
			if d then
				warn(`zins | adonis bypassed`)
			end

			return coroutine.yield(coroutine.running())
		end
		
		return o(...)
	end))

	setthreadidentity(7)
end)
getgenv().RapidFireEnabled = false
getgenv().is_firing = false
local originalCooldowns = {}
local utility = {}
--[[
    Copyright (c) 2025 [matcha]
    All rights reserved.

    This script is proprietary and confidential.
    Unauthorized copying, modification, distribution, or use of this code,
    via any medium, is strictly prohibited without prior written permission.

    Users: secured.11 | hookfunction
]]

--[[
    Made by samet

    Assign different flags to each element to prevent from configs overriding eachother
    Example script is at the bottom

    Documentation:
    function Library:Window(Data: table
        Name/name: string,
        Size/size: UDim2
    )

    function Window:Page(Data: table
        Name/name: string,
        Columns/columns: number,
        SubTabs/subtabs: boolean
    )

    function Page:SubPage(Data: table
        Icon/icon: string,
        Columns/columns: number
    )

    function Page:Section(Data: table
        Name/name: string,
        Side/side: number,
    )

    function Page:MultiSection(Data: table
        Sections/sections: table,
        Side/side: number
    )

    function Page:ScrollableSection(Data: table
        Name/name: string,
        Side/side: number,
        Size/size: number
    )

    function Section:Divider()

    function Section:Label(Data: table
        Name/name: string,
        Alignment/alignment: string
    )

    function Section:Toggle(Data: table
        Name/name: string,
        Default/default: boolean,
        Flag/flag: string,
        Callback/callback: function
    )

    function Section:Button(Data: table
        Name/name: string,
        Callback/callback: function
    )

    function Section:Slider(Data: table
        Name/name: string,
        Min/min: number,
        Max/max: number,
        Decimals/decimals: number,
        Default/default: number,
        Suffix/suffix: string,
        Flag/flag: string,
        Callback/callback: function
    )

    function Section:Textbox(Data: table
        Name/name: string,
        Default/default: string,
        Placeholder/placeholder: string,
        Flag/flag: string,
        Callback/callback: function
    )

    function Section:Dropdown(Data: table
        Name/name: string,
        Items/items: table,
        Default/default: string,
        Flag/flag: string,
        Multi/multi: boolean,
        Callback/callback: function
    )

    function Section:Listbox(Data: table
        Size/size: number,
        Items/items: table,
        Default/default: string,
        Multi/multi: boolean,
        Flag/flag: string,
        Callback/callback: function
    )

    function Label:Keybind(Data: table
        Name/name: string,
        Mode/mode: string,
        Default/default: EnumItem,
        Flag/flag: string,
        Callback/callback: function
    )

    function Label:Colorpicker(Data: table
        Name/name: string,
        Default/default: Color3,
        Alpha/alpha: boolean,
        Flag/flag: string,
        Callback/callback: function
    )

    function Toggle:Colorpicker(Data: table
        Name/name: string,
        Default/default: Color3,
        Alpha/alpha: boolean,
        Flag/flag: string,
        Callback/callback: function
    )

    function Toggle:Keybind(Data: table
        Name/name: string,
        Mode/mode: string,
        Default/default: EnumItem,
        Flag/flag: string,
        Callback/callback: function
    )

    function Sections:Textbox(Data: table
        Name/name: string,
        Default/default: string,
        Placeholder/placeholder: string,
        Flag/flag: string,
        Callback/callback: function
    )

    function Library:Watermark(Name: string)
    function Library:Notification(Text: string, Duration: number, Color: Color3, Icon: table)
    function Library:KeybindList()
]]

local LoadingTick = os.clock()

if getgenv().Library then 
    getgenv().Library:Unload()
end

local Library do
    local UserInputService = game:GetService("UserInputService")
    local Players = game:GetService("Players")
    local Workspace = game:GetService("Workspace")
    local HttpService = game:GetService("HttpService")
    local TweenService = game:GetService("TweenService")
    local CoreGui = cloneref and cloneref(game:GetService("CoreGui")) or game:GetService("CoreGui")

    gethui = gethui or function()
        return CoreGui
    end

    local LocalPlayer = Players.LocalPlayer
    local Camera = Workspace.CurrentCamera
    local Mouse = LocalPlayer:GetMouse()

    local FromRGB = Color3.fromRGB
    local FromHSV = Color3.fromHSV
    local FromHex = Color3.fromHex

    local RGBSequence = ColorSequence.new
    local RGBSequenceKeypoint = ColorSequenceKeypoint.new

    local NumSequence = NumberSequence.new
    local NumSequenceKeypoint = NumberSequenceKeypoint.new

    local UDim2New = UDim2.new
    local UDimNew = UDim.new
    local Vector2New = Vector2.new

    local InstanceNew = Instance.new

    local MathClamp = math.clamp
    local MathFloor = math.floor

    local TableInsert = table.insert
    local TableFind = table.find
    local TableRemove = table.remove
    local TableConcat = table.concat
    local TableUnpack = table.unpack

    local StringFormat = string.format
    local StringFind = string.find
    local StringGSub = string.gsub

    Library = {
        Flags = { },
        
        Theme = {
            ["Background"] = FromRGB(15, 15, 15),
            ["Inline"] = FromRGB(20, 20, 20),
            ["Page Background"] = FromRGB(30, 30, 30),
            ["Border"] = FromRGB(10, 10, 10),
            ["Outline"] = FromRGB(27, 27, 27),
            ["Accent"] = FromRGB(198, 154, 196),
            ["Element"] = FromRGB(33, 33, 33),
            ["Hovered Element"] = FromRGB(40, 40, 40),
            ["Text"] = FromRGB(215, 215, 215),
            ["Text Border"] = FromRGB(0, 0, 0)
        },

        MenuKeybind = Enum.KeyCode.Z, 

        Tween = {
            Time = 0.3,
            Style = Enum.EasingStyle.Exponential,
            Direction = Enum.EasingDirection.Out
        },

        Folders = {
            Directory = "matcha",
            Configs = "matcha/Configs",
            Assets = "matcha/Assets"
        },

        Images = { -- you're welcome to reupload the images and replace it with your own links
            ["Saturation"] = {"Saturation.png", "https://github.com/sametexe001/images/blob/main/saturation.png?raw=true" },
            ["Value"] = { "Value.png", "https://github.com/sametexe001/images/blob/main/value.png?raw=true" },
            ["Hue"] = { "Hue.png", "https://github.com/sametexe001/images/blob/main/hue.png?raw=true" },
            ["Scrollbar"] =  { "Scrollbar.png", "https://github.com/sametexe001/images/blob/main/scrollbar.png?raw=true" },
            ["Checkers"] = { "Checkers.png", "https://github.com/sametexe001/images/blob/main/checkers.png?raw=true" },
            ["Resize"] = { "Resize.png", "https://github.com/sametexe001/images/blob/main/resize.png?raw=true" },
        },

        -- Ignore below
        Pages = { },
        Sections = { },
        Connections = { },
        Threads = { },
        ThemeMap = { },
        ThemeItems = { },

        SetFlags = { },

        UnnamedConnections = 0,
        UnnamedFlags = 0,

        Holder = nil,
        NotifHolder = nil,
        Font = nil,
        KeyList = nil,

        CurrentColorpicker = nil
    }

    Library.__index = Library
    Library.Sections.__index = Library.Sections
    Library.Pages.__index = Library.Pages

    local Keys = {
        ["Unknown"]           = "Unknown",
        ["Backspace"]         = "Back",
        ["Tab"]               = "Tab",
        ["Clear"]             = "Clear",
        ["Return"]            = "Return",
        ["Pause"]             = "Pause",
        ["Escape"]            = "Escape",
        ["Space"]             = "Space",
        ["QuotedDouble"]      = '"',
        ["Hash"]              = "#",
        ["Dollar"]            = "$",
        ["Percent"]           = "%",
        ["Ampersand"]         = "&",
        ["Quote"]             = "'",
        ["LeftParenthesis"]   = "(",
        ["RightParenthesis"]  = " )",
        ["Asterisk"]          = "*",
        ["Plus"]              = "+",
        ["Comma"]             = ",",
        ["Minus"]             = "-",
        ["Period"]            = ".",
        ["Slash"]             = "`",
        ["Three"]             = "3",
        ["Seven"]             = "7",
        ["Eight"]             = "8",
        ["Colon"]             = ":",
        ["Semicolon"]         = ";",
        ["LessThan"]          = "<",
        ["GreaterThan"]       = ">",
        ["Question"]          = "?",
        ["Equals"]            = "=",
        ["At"]                = "@",
        ["LeftBracket"]       = "LeftBracket",
        ["RightBracket"]      = "RightBracked",
        ["BackSlash"]         = "BackSlash",
        ["Caret"]             = "^",
        ["Underscore"]        = "_",
        ["Backquote"]         = "`",
        ["LeftCurly"]         = "{",
        ["Pipe"]              = "|",
        ["RightCurly"]        = "}",
        ["Tilde"]             = "~",
        ["Delete"]            = "Delete",
        ["End"]               = "End",
        ["KeypadZero"]        = "Keypad0",
        ["KeypadOne"]         = "Keypad1",
        ["KeypadTwo"]         = "Keypad2",
        ["KeypadThree"]       = "Keypad3",
        ["KeypadFour"]        = "Keypad4",
        ["KeypadFive"]        = "Keypad5",
        ["KeypadSix"]         = "Keypad6",
        ["KeypadSeven"]       = "Keypad7",
        ["KeypadEight"]       = "Keypad8",
        ["KeypadNine"]        = "Keypad9",
        ["KeypadPeriod"]      = "KeypadP",
        ["KeypadDivide"]      = "KeypadD",
        ["KeypadMultiply"]    = "KeypadM",
        ["KeypadMinus"]       = "KeypadM",
        ["KeypadPlus"]        = "KeypadP",
        ["KeypadEnter"]       = "KeypadE",
        ["KeypadEquals"]      = "KeypadE",
        ["Insert"]            = "Insert",
        ["Home"]              = "Home",
        ["PageUp"]            = "PageUp",
        ["PageDown"]          = "PageDown",
        ["RightShift"]        = "RightShift",
        ["LeftShift"]         = "LeftShift",
        ["RightControl"]      = "RightControl",
        ["LeftControl"]       = "LeftControl",
        ["LeftAlt"]           = "LeftAlt",
        ["RightAlt"]          = "RightAlt"
    }

    -- Files 
    for _, FileName in Library.Folders do
        if not isfolder(FileName) then
            makefolder(FileName)
        end
    end

    for _, ImageData in Library.Images do
        local ImageName = ImageData[1]
        local ImageLink = ImageData[2]
        
        if not isfile(Library.Folders.Assets .. "/" .. ImageName) then
            writefile(Library.Folders.Assets .. "/" .. ImageName, game:HttpGet(ImageLink))
        end
    end

    local Tween = { } do
        Tween.__index = Tween

        Tween.Create = function(self, Item, Info, Goal, IsRawItem)
            Item = IsRawItem and Item or Item.Instance
            Info = Info or TweenInfo.new(Library.Tween.Time, Library.Tween.Style, Library.Tween.Direction)

            local NewTween = {
                Tween = TweenService:Create(Item, Info, Goal),
                Info = Info,
                Goal = Goal,
                Item = Item
            }

            NewTween.Tween:Play()

            setmetatable(NewTween, Tween)

            return NewTween
        end

        Tween.Get = function(self)
            if not self.Tween then 
                return
            end

            return self.Tween, self.Info, self.Goal
        end

        Tween.Pause = function(self)
            if not self.Tween then 
                return
            end

            self.Tween:Pause()
        end

        Tween.Play = function(self)
            if not self.Tween then 
                return
            end

            self.Tween:Play()
        end

        Tween.Clean = function(self)
            if not self.Tween then 
                return
            end

            Tween:Pause()
            self = nil
        end
    end

    local Instances = { } do
        Instances.__index = Instances

        Instances.Create = function(self, Class, Properties)
            local NewItem = {
                Instance = InstanceNew(Class),
                Properties = Properties,
                Class = Class
            }

            setmetatable(NewItem, Instances)

            for Property, Value in NewItem.Properties do
                NewItem.Instance[Property] = Value
            end

            return NewItem
        end

        Instances.Border = function(self)
            if not self.Instance then 
                return
            end

            local Item = self.Instance
            local UIStroke = Instances:Create("UIStroke", {
                Parent = Item,
                Color = Library.Theme.Border,
                Thickness = 1,
                LineJoinMode = Enum.LineJoinMode.Miter
            })

            UIStroke:AddToTheme({Color = "Border"})

            return UIStroke
        end

        Instances.AddToTheme = function(self, Properties)
            if not self.Instance then 
                return
            end

            Library:AddToTheme(self, Properties)
        end

        Instances.ChangeItemTheme = function(self, Properties)
            if not self.Instance then 
                return
            end

            Library:ChangeItemTheme(self, Properties)
        end

        Instances.Connect = function(self, Event, Callback, Name)
            if not self.Instance then 
                return
            end

            if not self.Instance[Event] then 
                return
            end

            return Library:Connect(self.Instance[Event], Callback, Name)
        end

        Instances.Tween = function(self, Info, Goal)
            if not self.Instance then 
                return
            end

            return Tween:Create(self, Info, Goal)
        end

        Instances.Disconnect = function(self, Name)
            if not self.Instance then 
                return
            end

            return Library:Disconnect(Name)
        end

        Instances.Clean = function(self)
            if not self.Instance then 
                return
            end

            self.Instance:Destroy()
            self = nil
        end

        Instances.MakeDraggable = function(self)
            if not self.Instance then 
                return
            end

            local Gui = self.Instance

            local Dragging = false 
            local DragStart
            local StartPosition 

            local Set = function(Input)
                local DragDelta = Input.Position - DragStart
                self:Tween(TweenInfo.new(0.16, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Position = UDim2New(StartPosition.X.Scale, StartPosition.X.Offset + DragDelta.X, StartPosition.Y.Scale, StartPosition.Y.Offset + DragDelta.Y)})
            end

            self:Connect("InputBegan", function(Input)
                if Input.UserInputType == Enum.UserInputType.MouseButton1 or Input.UserInputType == Enum.UserInputType.Touch then
                    Dragging = true

                    DragStart = Input.Position
                    StartPosition = Gui.Position
                end
            end)

            self:Connect("InputEnded", function(Input)
                if Input.UserInputType == Enum.UserInputType.MouseButton1 or Input.UserInputType == Enum.UserInputType.Touch then
                    Dragging = false
                end
            end)

            Library:Connect(UserInputService.InputChanged, function(Input)
                if Input.UserInputType == Enum.UserInputType.MouseMovement or Input.UserInputType == Enum.UserInputType.Touch then
                    if Dragging then
                        Set(Input)
                    end
                end
            end)

            return Dragging
        end

        Instances.MakeResizeable = function(self, Minimum, Maximum)
            if not self.Instance then 
                return
            end

            local Gui = self.Instance

            local Resizing = false 
            local Start = UDim2New()
            local Delta = UDim2New()
            local ResizeMax = Gui.Parent.AbsoluteSize - Gui.AbsoluteSize

            local ResizeButton = Instances:Create("TextButton", {
				Parent = Gui,
				AnchorPoint = Vector2New(1, 1),
				BorderColor3 = FromRGB(0, 0, 0),
				Size = UDim2New(0, 8, 0, 8),
				Position = UDim2New(1, 0, 1, 0),
                Name = "\0",
				BorderSizePixel = 0,
				BackgroundTransparency = 1,
				AutoButtonColor = false,
                Visible = true,
                Text = ""
			})

            ResizeButton:Connect("InputBegan", function(Input)
                if Input.UserInputType == Enum.UserInputType.MouseButton1 or Input.UserInputType == Enum.UserInputType.Touch then
                    Resizing = true

                    Start = Gui.Size - UDim2New(0, Input.Position.X, 0, Input.Position.Y)
                end
            end)

            ResizeButton:Connect("InputEnded", function(Input)
                if Input.UserInputType == Enum.UserInputType.MouseButton1 or Input.UserInputType == Enum.UserInputType.Touch then
                    Resizing = false
                end
            end)

            Library:Connect(UserInputService.InputChanged, function(Input)
                if Input.UserInputType == Enum.UserInputType.MouseMovement and Resizing then
					ResizeMax = Maximum or Gui.Parent.AbsoluteSize - Gui.AbsoluteSize

					Delta = Start + UDim2New(0, Input.Position.X, 0, Input.Position.Y)
					Delta = UDim2New(0, math.clamp(Delta.X.Offset, Minimum.X, ResizeMax.X), 0, math.clamp(Delta.Y.Offset, Minimum.Y, ResizeMax.Y))

					Tween:Create(Gui, TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Size = Delta}, true)
                end
            end)

            return Resizing
        end

        Instances.OnHover = function(self, Function)
            if not self.Instance then 
                return
            end
            
            return Library:Connect(self.Instance.MouseEnter, Function)
        end

        Instances.OnHoverLeave = function(self, Function)
            if not self.Instance then 
                return
            end
            
            return Library:Connect(self.Instance.MouseLeave, Function)
        end
    end

    local CustomFont = { } do
        function CustomFont:New(Name, Weight, Style, Data)
            if isfile(Library.Folders.Assets .. "/" .. Name .. ".json") then
                return Font.new(getcustomasset(Library.Folders.Assets .. "/" .. Name .. ".json"))
            end

            if not isfile(Library.Folders.Assets .. "/" .. Name .. ".ttf") then 
                writefile(Library.Folders.Assets .. "/" .. Name .. ".ttf", game:HttpGet(Data.Url))
            end

            local FontData = {
                name = Name,
                faces = { {
                    name = "Regular",
                    weight = Weight,
                    style = Style,
                    assetId = getcustomasset(Library.Folders.Assets .. "/" .. Name .. ".ttf")
                } }
            }

            writefile(Library.Folders.Assets .. "/" .. Name .. ".json", HttpService:JSONEncode(FontData))
            return Font.new(getcustomasset(Library.Folders.Assets .. "/" .. Name .. ".json"))
        end

        function CustomFont:Get(Name)
            if isfile(Library.Folders.Assets .. "/" .. Name .. ".json") then
                return Font.new(getcustomasset(Library.Folders.Assets .. "/" .. Name .. ".json"))
            end
        end

        CustomFont:New("Windows-XP-Tahoma", 200, "Regular", {
            Url = "https://github.com/sametexe001/luas/raw/refs/heads/main/fonts/windows-xp-tahoma.ttf"
        })

        Library.Font = CustomFont:Get("Windows-XP-Tahoma")
    end

    Library.Holder = Instances:Create("ScreenGui", {
        Parent = gethui(),
        Name = "\0",
        ResetOnSpawn = false
    })

    Library.NotifHolder = Instances:Create("Frame", {
        Parent = Library.Holder.Instance,
        BorderColor3 = FromRGB(0, 0, 0),
        AnchorPoint = Vector2New(0.5, 0),
        BackgroundTransparency = 1,
        Position = UDim2New(0.5, 0, 0, 0),
        Name = "\0",
        Size = UDim2New(0.34, 0, 1, -14),
        BorderSizePixel = 0,
        BackgroundColor3 = FromRGB(255, 255, 255)
    }) 
    
    Instances:Create("UIListLayout", {
        Parent = Library.NotifHolder.Instance,
        VerticalAlignment = Enum.VerticalAlignment.Top,
        SortOrder = Enum.SortOrder.LayoutOrder,
        HorizontalAlignment = Enum.HorizontalAlignment.Center,
        Padding = UDimNew(0, 10)
    }) 

    Library.GetImage = function(self, Image)
        local ImageData = self.Images[Image]

        if not ImageData then 
            return
        end

        return getcustomasset(self.Folders.Assets .. "/" .. ImageData[1])
    end

    Library.Round = function(self, Number, Float)
        local Multiplier = 1 / (Float or 1)
        return MathFloor(Number * Multiplier) / Multiplier
    end

    Library.GetTransparencyPropertyFromItem = function(self, Item)
        if Item:IsA("Frame") then
            return { "BackgroundTransparency" }
        elseif Item:IsA("TextLabel") or Item:IsA("TextButton") then
            return { "TextTransparency", "BackgroundTransparency" }
        elseif Item:IsA("ImageLabel") or Item:IsA("ImageButton") then
            return { "BackgroundTransparency", "ImageTransparency" }
        elseif Item:IsA("ScrollingFrame") then
            return { "BackgroundTransparency", "ScrollBarImageTransparency" }
        elseif Item:IsA("TextBox") then
            return { "TextTransparency", "BackgroundTransparency" }
        elseif Item:IsA("UIStroke") then 
            return { "Transparency" }
        end
    end

    Library.FadeItem = function(self, Item, Property, Visibility, Speed)
        local OldTransparency = Item[Property]
        Item[Property] = Visibility and 1 or OldTransparency

        local NewTween = Tween:Create(Item, TweenInfo.new(Speed or Library.Tween.Time, Library.Tween.Style, Library.Tween.Direction), {
            [Property] = Visibility and OldTransparency or 1
        }, true)

        Library:Connect(NewTween.Tween.Completed, function()
            if not Visibility then 
                task.wait()
                Item[Property] = OldTransparency
            end
        end)

        return NewTween
    end

    Library.Unload = function(self)
        for Index, Value in self.Connections do 
            Value.Connection:Disconnect()
        end

        for Index, Value in self.Threads do 
            coroutine.close(Value)
        end

        if self.Holder then 
            self.Holder:Clean()
        end

        Library = nil 
        getgenv().Library = nil
    end

    Library.Thread = function(self, Function)
        local NewThread = coroutine.create(Function)
        
        coroutine.wrap(function()
            coroutine.resume(NewThread)
        end)()

        TableInsert(self.Threads, NewThread)

        return NewThread
    end
    
    Library.SafeCall = function(self, Function, ...)
        local Arguements = { ... }
        local Success, Result = pcall(Function, TableUnpack(Arguements))

        if not Success then
            Library:Notification("Error caught in function, report this to the devs:\n"..Result, 5, FromRGB(255, 0, 0))
            warn(Result)
            return false
        end

        return Success
    end

    Library.Connect = function(self, Event, Callback, Name)
        Name = Name or StringFormat("Connection_%s_%s", self.UnnamedConnections + 1, HttpService:GenerateGUID(false))

        local NewConnection = {
            Event = Event,
            Callback = Callback,
            Name = Name,
            Connection = nil
        }

        Library:Thread(function()
            NewConnection.Connection = Event:Connect(Callback)
        end)

        TableInsert(self.Connections, NewConnection)
        return NewConnection
    end

    Library.Disconnect = function(self, Name)
        for _, Connection in self.Connections do 
            if Connection.Name == Name then
                Connection.Connection:Disconnect()
                break
            end
        end
    end

    Library.NextFlag = function(self)
        local FlagNumber = self.UnnamedFlags + 1
        return StringFormat("Flag Number %s %s", FlagNumber, HttpService:GenerateGUID(false))
    end

    Library.AddToTheme = function(self, Item, Properties)
        Item = Item.Instance or Item 

        local ThemeData = {
            Item = Item,
            Properties = Properties,
        }

        for Property, Value in ThemeData.Properties do
            if type(Value) == "string" then
                Item[Property] = self.Theme[Value]
            end
        end

        TableInsert(self.ThemeItems, ThemeData)
        self.ThemeMap[Item] = ThemeData
    end

    Library.GetConfig = function(self)
        local Config = { } 

        local Success, Result = Library:SafeCall(function()
            for Index, Value in Library.Flags do 
                if type(Value) == "table" and Value.Key then
                    Config[Index] = {Key = tostring(Value.Key), Mode = Value.Mode}
                elseif type(Value) == "table" and Value.Color then
                    Config[Index] = {Color = "#" .. Value.HexValue, Alpha = Value.Alpha}
                else
                    Config[Index] = Value
                end
            end
        end)

        return HttpService:JSONEncode(Config)
    end

    Library.LoadConfig = function(self, Config)
        local Decoded = HttpService:JSONDecode(Config)

        local Success, Result = Library:SafeCall(function()
            for Index, Value in Decoded do 
                local SetFunction = Library.SetFlags[Index]

                if not SetFunction then
                    continue
                end

                if type(Value) == "table" and Value.Key then 
                    SetFunction(Value)
                elseif type(Value) == "table" and Value.Color then
                    SetFunction(Value.Color, Value.Alpha)
                else
                    SetFunction(Value)
                end
            end
        end)

        if Success then 
            Library:Notification("Successfully loaded config", 5, Color3.fromRGB(0, 255, 0))
        end
    end

    Library.DeleteConfig = function(self, Config)
        if isfile(Library.Folders.Configs .. "/" .. Config) then 
            delfile(Library.Folders.Configs .. "/" .. Config)
            Library:Notification("Deleted config " .. Config .. ".json", 5, Color3.fromRGB(0, 255, 0))
        end
    end

    Library.SaveConfig = function(self, Config)
        if isfile(Library.Folders.Directory .. "/" .. Library.Folders.Configs .. "/" .. Config .. ".json") then
            writefile(Library.Folders.Directory .. "/" .. Library.Folders.Configs .. "/" .. Config .. ".json", Library:GetConfig())
            Library:Notification("Saved config " .. Config .. ".json", 5, Color3.fromRGB(0, 255, 0))
        end
    end

    Library.RefreshConfigsList = function(self, Element)
        local CurrentList = { }
        local List = { }

        local ConfigFolderName = StringGSub(Library.Folders.Configs, Library.Folders.Directory .. "/", "")

        for Index, Value in listfiles(Library.Folders.Configs) do
            local FileName = StringGSub(Value, Library.Folders.Directory .. "\\" .. ConfigFolderName .. "\\", "")
            List[Index] = FileName
        end

        local IsNew = #List ~= CurrentList

        if not IsNew then
            for Index = 1, #List do
                if List[Index] ~= CurrentList[Index] then
                    IsNew = true
                    break
                end
            end
        else
            CurrentList = List
            Element:Refresh(CurrentList)
        end
    end

    Library.ChangeItemTheme = function(self, Item, Properties)
        Item = Item.Instance or Item

        if not self.ThemeMap[Item] then 
            return
        end

        self.ThemeMap[Item].Properties = Properties
        self.ThemeMap[Item] = self.ThemeMap[Item]
    end

    Library.ChangeTheme = function(self, Theme, Color)
        self.Theme[Theme] = Color

        for _, Item in self.ThemeItems do
            for Property, Value in Item.Properties do
                if type(Value) == "string" and Value == Theme then
                    Item.Item[Property] = Color
                end
            end
        end
    end

    Library.IsMouseOverFrame = function(self, Frame)
        Frame = Frame.Instance

        local MousePosition = Vector2New(Mouse.X, Mouse.Y)

        return MousePosition.X >= Frame.AbsolutePosition.X and MousePosition.X <= Frame.AbsolutePosition.X + Frame.AbsoluteSize.X 
        and MousePosition.Y >= Frame.AbsolutePosition.Y and MousePosition.Y <= Frame.AbsolutePosition.Y + Frame.AbsoluteSize.Y
    end

    Library.Watermark = function(self, Name)
        local Watermark = { } 

        local Items = { } do 
            Items["Watermark"] = Instances:Create("Frame", {
                Parent = Library.Holder.Instance,
                Size = UDim2New(0, 0, 0, 20),
                Name = "\0",
                Position = UDim2New(0, 15, 0, 15),
                BorderColor3 = FromRGB(10, 10, 10),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.X,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["Watermark"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})

            Items["Watermark"]:MakeDraggable()
            
            Instances:Create("UIStroke", {
                Parent = Items["Watermark"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Instances:Create("UIPadding", {
                Parent = Items["Watermark"].Instance,
                PaddingTop = UDimNew(0, 2),
                PaddingRight = UDimNew(0, 5),
                PaddingLeft = UDimNew(0, 5)
            }) 
            
            Items["Title"] = Instances:Create("TextLabel", {
                Parent = Items["Watermark"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Name,
                Name = "\0",
                Size = UDim2New(1, 0, 0, 15),
                BackgroundTransparency = 1,
                Position = UDim2New(0, 0, 0, 1),
                BorderSizePixel = 0,
                AutomaticSize = Enum.AutomaticSize.X,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Title"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Title"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["AccentLine"] = Instances:Create("Frame", {
                Parent = Items["Watermark"].Instance,
                Name = "\0",
                Position = UDim2New(0, -5, 0, -2),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 10, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(235, 157, 255)
            })  Items["AccentLine"]:AddToTheme({BackgroundColor3 = "Accent"})
            
            Instances:Create("UIGradient", {
                Parent = Items["AccentLine"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(65, 65, 65))}
            })             
        end

        function Watermark:SetVisibility(Bool)
            Items["Watermark"].Instance.Visible = Bool
        end
        
        return Watermark
    end

    Library.Notification = function(self, Text, Duration, Color, Icon)
        local Items = { } do
            Items["Notification"] = Instances:Create("Frame", {
                Parent = Library.NotifHolder.Instance,
                Name = "\0",
                Size = UDim2New(0, 0, 0, 22),
                BorderColor3 = FromRGB(10, 10, 10),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.X,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["Notification"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Notification"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"}) 
            
            Instances:Create("UIPadding", {
                Parent = Items["Notification"].Instance,
                PaddingTop = UDimNew(0, 1),
                PaddingRight = UDimNew(0, 8),
                PaddingLeft = UDimNew(0, 5)
            }) 
            
            Items["Title"] = Instances:Create("TextLabel", {
                Parent = Items["Notification"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Text,
                Name = "\0",
                Size = UDim2New(1, 0, 0, 15),
                BackgroundTransparency = 1,
                Position = UDim2New(0, 13, 0, 2),
                BorderSizePixel = 0,
                AutomaticSize = Enum.AutomaticSize.X,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Title"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Title"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})

            Items["AccentLine"] = Instances:Create("Frame", {
                Parent = Items["Notification"].Instance,
                Name = "\0",
                Position = UDim2New(0, -5, 0, -1),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 13, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = Color
            })  
            
            Instances:Create("UIGradient", {
                Parent = Items["AccentLine"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(65, 65, 65))}
            })
            
            Items["Icon"] = Instances:Create("ImageLabel", {
                Parent = Items["Notification"].Instance,
                ImageColor3 = FromRGB(255, 255, 255),
                ScaleType = Enum.ScaleType.Fit,
                BorderColor3 = FromRGB(0, 0, 0),
                Name = "\0",
                Image = "rbxassetid://94324346713012",
                BackgroundTransparency = 1,
                Position = UDim2New(0, -2, 0, 3),
                Size = UDim2New(0, 13, 0, 13),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 

            if not Icon then 
                Items["Icon"]:Clean()
                Items["Title"].Instance.Position = UDim2New(0, 1, 0, 2)
            else
                Items["Icon"].Instance.Image = Icon[1]
                Items["Icon"].Instance.ImageColor3 = Icon[2] or FromRGB(255, 255, 255)
            end
        end

        Items["Notification"].Instance.BackgroundTransparency = 1
        Items["Notification"].Instance.Size = UDim2New(0, 0, 0, 0)
        for Index, Value in Items["Notification"].Instance:GetDescendants() do
            if Value:IsA("UIStroke") then 
                Value.Transparency = 1
            elseif Value:IsA("TextLabel") then 
                Value.TextTransparency = 1
            elseif Value:IsA("ImageLabel") then 
                Value.ImageTransparency = 1
            elseif Value:IsA("Frame") then 
                Value.BackgroundTransparency = 1
            end
        end

        Library:Thread(function()
            Items["Notification"]:Tween(nil, {BackgroundTransparency = 0, Size = UDim2New(0, 0, 0, 22)})
            
            task.wait(0.06)

            for Index, Value in Items["Notification"].Instance:GetDescendants() do
                if Value:IsA("UIStroke") then
                    Tween:Create(Value, nil, {Transparency = 0}, true)
                elseif Value:IsA("TextLabel") then
                    Tween:Create(Value, nil, {TextTransparency = 0}, true)
                elseif Value:IsA("ImageLabel") then
                    Tween:Create(Value, nil, {ImageTransparency = 0}, true)
                elseif Value:IsA("Frame") then
                    Tween:Create(Value, nil, {BackgroundTransparency = 0}, true)
                end
            end

            task.delay(Duration + 0.1, function()
                for Index, Value in Items["Notification"].Instance:GetDescendants() do
                    if Value:IsA("UIStroke") then
                        Tween:Create(Value, nil, {Transparency = 1}, true)
                    elseif Value:IsA("TextLabel") then
                        Tween:Create(Value, nil, {TextTransparency = 1}, true)
                    elseif Value:IsA("ImageLabel") then
                        Tween:Create(Value, nil, {ImageTransparency = 1}, true)
                    elseif Value:IsA("Frame") then
                        Tween:Create(Value, nil, {BackgroundTransparency = 1}, true)
                    end
                end

                task.wait(0.06)

                Items["Notification"]:Tween(nil, {BackgroundTransparency = 1, Size = UDim2New(0, 0, 0, 0)})

                task.wait(0.5)
                Items["Notification"]:Clean()
            end)
        end)
    end

    Library.KeybindList = function(self)
        local KeybindList = { }
        self.KeyList = KeybindList

        local Items = { } do
            Items["KeybindList"] = Instances:Create("Frame", {
                Parent = Library.Holder.Instance,
                BorderColor3 = FromRGB(10, 10, 10),
                AnchorPoint = Vector2New(0, 0.5),
                Name = "\0",
                Position = UDim2New(0, 15, 0.5, 0),
                Size = UDim2New(0, 0, 0, 18),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.XY,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["KeybindList"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})

            Items["KeybindList"]:MakeDraggable()
            
            Instances:Create("UIStroke", {
                Parent = Items["KeybindList"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["AccentLine"] = Instances:Create("Frame", {
                Parent = Items["KeybindList"].Instance,
                Name = "\0",
                Position = UDim2New(0, -5, 0, -5),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 10, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(235, 157, 255)
            })  Items["AccentLine"]:AddToTheme({BackgroundColor3 = "Accent"})
            
            Instances:Create("UIGradient", {
                Parent = Items["AccentLine"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(65, 65, 65))}
            }) 
            
            Instances:Create("UIPadding", {
                Parent = Items["KeybindList"].Instance,
                PaddingTop = UDimNew(0, 5),
                PaddingBottom = UDimNew(0, 5),
                PaddingRight = UDimNew(0, 5),
                PaddingLeft = UDimNew(0, 5)
            }) 
            
            Items["Title"] = Instances:Create("TextLabel", {
                Parent = Items["KeybindList"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "Keybinds",
                Name = "\0",
                Size = UDim2New(0, 100, 0, 15),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Position = UDim2New(0, 0, 0, -1),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Title"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Title"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Content"] = Instances:Create("Frame", {
                Parent = Items["KeybindList"].Instance,
                Name = "\0",
                BackgroundTransparency = 1,
                Position = UDim2New(0, 5, 0, 19),
                BorderColor3 = FromRGB(0, 0, 0),
                BorderSizePixel = 0,
                AutomaticSize = Enum.AutomaticSize.XY,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Instances:Create("UIListLayout", {
                Parent = Items["Content"].Instance,
                Padding = UDimNew(0, 4),
                SortOrder = Enum.SortOrder.LayoutOrder
            }) 
        end

        function KeybindList:Add(Mode, Name, Key)
            local NewKey = Instances:Create("TextLabel", {
                Parent = Items["Content"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "(" .. Mode .. ") " .. Name .. " - " .. Key,
                Name = "\0",
                Size = UDim2New(0, 0, 0, 15),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                BorderSizePixel = 0,
                AutomaticSize = Enum.AutomaticSize.X,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  NewKey:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = NewKey.Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
        
            function NewKey:Set(Mode, Name, Key)
                NewKey.Instance.Text = "(" .. Mode .. ") " .. Name .. " - " .. Key
            end

            function NewKey:SetStatus(Status)
                if Status == "Active" then 
                    NewKey:Tween(nil, {TextColor3 = Library.Theme.Accent})
                    NewKey:ChangeItemTheme({TextColor3 = "Accent"})
                else 
                    NewKey:Tween(nil, {TextColor3 = Library.Theme.Text})
                    NewKey:ChangeItemTheme({TextColor3 = "Text"})
                end
            end

            return NewKey
        end

        function KeybindList:SetVisibility(Bool)
            Items["KeybindList"].Instance.Visible = Bool
        end

        return KeybindList
    end

    Library.CreateColorpicker = function(self, Data)
        local Colorpicker = {
            Hue = 0,
            Saturation = 0,
            Value = 0,

            Alpha = 0,

            HexValue = "",
            
            IsOpen = false,

            Color = FromRGB(0, 0, 0),

            Class = "Colorpicker"
        }

        Library.Flags[Data.Flag] = { }

        local Items = { } do
            Items["ColorpickerButton"] = Instances:Create("TextButton", {
                Parent = Data.Parent.Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "",
                AutoButtonColor = false,
                AnchorPoint = Vector2New(1, 0.5),
                Name = "\0",
                Position = UDim2New(1, 0, 0.5, 0),
                Size = UDim2New(0, 20, 0, 10),
                BorderSizePixel = 0,
                TextSize = 14,
                BackgroundColor3 = FromRGB(255, 0, 0)
            }) 


            Colorpicker.CalculateCount = function(self, Index, YScale, YOffset)
                local MaxButtonsAdded = 5

                local Column = Index % MaxButtonsAdded
            
                local ButtonSize = Items["ColorpickerButton"].Instance.AbsoluteSize
                local Spacing = 4
            
                local XPosition = (ButtonSize.X + Spacing) * Column - Spacing - 21
            
                Items["ColorpickerButton"].Instance.Position = UDim2New(1, -XPosition, YScale or 0.5, YOffset or 0)
            end

            Colorpicker:CalculateCount(Data.Count)
            
            Instances:Create("UIStroke", {
                Parent = Items["ColorpickerButton"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Instances:Create("UIGradient", {
                Parent = Items["ColorpickerButton"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(100, 100, 100))}
            })             

            Items["ColorpickerWindow"] = Instances:Create("TextButton", {
                Parent = Library.Holder.Instance,
                AutoButtonColor = false,
                Text = "",
                Name = "\0",
                Position = UDim2New(0, Data.Parent.Instance.AbsolutePosition.X, 0, Data.Parent.Instance.AbsolutePosition.Y + 15),
                BorderColor3 = FromRGB(10, 10, 10),
                Visible = false,
                Size = UDim2New(0, 238, 0, 224),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["ColorpickerWindow"]:AddToTheme({BackgroundColor3 = "Background"})
            
            Items["ColorpickerWindow"]:MakeDraggable()
            Items["ColorpickerWindow"]:MakeResizeable(Vector2New(200, 180), Vector2New(9999, 9999))

            Instances:Create("UIStroke", {
                Parent = Items["ColorpickerWindow"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["Title"] = Instances:Create("TextLabel", {
                Parent = Items["ColorpickerWindow"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Data.Name,
                Name = "\0",
                Size = UDim2New(1, 0, 0, 15),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Position = UDim2New(0, -2, 0, -3),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Title"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Title"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["AccentLine"] = Instances:Create("Frame", {
                Parent = Items["ColorpickerWindow"].Instance,
                Name = "\0",
                Position = UDim2New(0, -6, 0, -6),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 12, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(235, 157, 255)
            })  Items["AccentLine"]:AddToTheme({BackgroundColor3 = "Accent"})
            
            Instances:Create("UIGradient", {
                Parent = Items["AccentLine"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(65, 65, 65))}
            }) 
            
            Instances:Create("UIPadding", {
                Parent = Items["ColorpickerWindow"].Instance,
                PaddingTop = UDimNew(0, 6),
                PaddingBottom = UDimNew(0, 6),
                PaddingRight = UDimNew(0, 6),
                PaddingLeft = UDimNew(0, 6)
            }) 
            
            Items["Palette"] = Instances:Create("TextButton", {
                Parent = Items["ColorpickerWindow"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "",
                AutoButtonColor = false,
                Name = "\0",
                Position = UDim2New(0, 0, 0, 15),
                Size = UDim2New(1, -26, 1, -40),
                BorderSizePixel = 0,
                TextSize = 14,
                BackgroundColor3 = FromRGB(255, 0, 0)
            }) 
            
            Items["Saturation"] = Instances:Create("ImageLabel", {
                Parent = Items["Palette"].Instance,
                BorderColor3 = FromRGB(0, 0, 0),
                Image = Library:GetImage("Saturation"),
                BackgroundTransparency = 1,
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["Value"] = Instances:Create("ImageLabel", {
                Parent = Items["Palette"].Instance,
                BorderColor3 = FromRGB(0, 0, 0),
                Image = Library:GetImage("Value"),
                BackgroundTransparency = 1,
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["Palette"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["PaletteDragger"] = Instances:Create("Frame", {
                Parent = Items["Palette"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(0, 2, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["PaletteDragger"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["Hue"] = Instances:Create("ImageButton", {
                Parent = Items["ColorpickerWindow"].Instance,
                BorderColor3 = FromRGB(0, 0, 0),
                AutoButtonColor = false,
                AnchorPoint = Vector2New(1, 0),
                Image = Library:GetImage("Hue"),
                Name = "\0",
                Position = UDim2New(1, 0, 0, 15),
                Size = UDim2New(0, 18, 1, -15),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["HueDragger"] = Instances:Create("Frame", {
                Parent = Items["Hue"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 1),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["HueDragger"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Hue"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["Alpha"] = Instances:Create("TextButton", {
                Parent = Items["ColorpickerWindow"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "",
                AutoButtonColor = false,
                AnchorPoint = Vector2New(0, 1),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 0),
                Size = UDim2New(1, -26, 0, 18),
                BorderSizePixel = 0,
                TextSize = 14,
                BackgroundColor3 = FromRGB(255, 0, 0)
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["Alpha"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["Checkers"] = Instances:Create("ImageLabel", {
                Parent = Items["Alpha"].Instance,
                ScaleType = Enum.ScaleType.Tile,
                BorderColor3 = FromRGB(0, 0, 0),
                Image = Library:GetImage("Checkers"),
                TileSize = UDim2New(0, 6, 0, 6),
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Instances:Create("UIGradient", {
                Parent = Items["Checkers"].Instance,
                Transparency = NumSequence{NumSequenceKeypoint(0, 1), NumSequenceKeypoint(1, 0)}
            }) 
            
            Instances:Create("UIGradient", {
                Parent = Items["Alpha"].Instance,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(0, 0, 0))}
            }) 
            
            Items["AlphaDragger"] = Instances:Create("Frame", {
                Parent = Items["Alpha"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(0, 1, 1, 0),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["AlphaDragger"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
        end

        local SlidingPalette = false
        local SlidingHue = false
        local SlidingAlpha = false

        local Debounce = false

        function Colorpicker:SetOpen(Bool)
            if Debounce then 
                return 
            end

            Colorpicker.IsOpen = Bool

            Debounce = true 

            if Bool then 
                Items["ColorpickerWindow"].Instance.Visible = true
                Items["ColorpickerWindow"].Instance.Position = UDim2New(0, Data.Parent.Instance.AbsolutePosition.X, 0, Data.Parent.Instance.AbsolutePosition.Y + 15)

                if Library.CurrentColorpicker then
                    Library.CurrentColorpicker:SetOpen(false)
                    Library.CurrentColorpicker = nil 
                end

                if not Library.CurrentColorpicker then 
                    Library.CurrentColorpicker = Colorpicker
                end
            else
                Library.CurrentColorpicker = nil
            end

            local Descendants = Items["ColorpickerWindow"].Instance:GetDescendants()
            TableInsert(Descendants, Items["ColorpickerWindow"].Instance)

            local NewTween
            for Index, Value in Descendants do 
                local ValueIndex = Library:GetTransparencyPropertyFromItem(Value)

                if not ValueIndex then 
                    continue
                end

                if not StringFind(Value.ClassName, "UI") then 
                    Value.ZIndex = Bool and 10001 or 1
                end

                if type(ValueIndex) == "table" then
                    for _, Property in ValueIndex do 
                        NewTween = Library:FadeItem(Value, Property, Bool, Data.FadeSpeed)
                    end
                else
                    NewTween = Library:FadeItem(Value, ValueIndex, Bool, Data.FadeSpeed)
                end
            end

            Library:Connect(NewTween.Tween.Completed, function()
                Debounce = false
                Items["ColorpickerWindow"].Instance.Visible = Bool
            end)
        end

        function Colorpicker:Get()
            return Colorpicker.Value
        end

        function Colorpicker:SetVisibility(Bool)
           Data.Parent.Instance.Visible = Bool 
        end

        function Colorpicker:Set(Color, Alpha)
            if type(Color) == "table" then 
                Color = FromRGB(Color[1], Color[2], Color[3])
                Alpha = Color[4]
            elseif type(Color) == "string" then 
                Color = FromHex(Color)
            end

            self.Hue, self.Saturation, self.Value = Color:ToHSV()
            self.Alpha = Alpha or 0

            self.Color = FromHSV(self.Hue, self.Saturation, self.Value)
            self.HexValue = self.Color:ToHex()

            Library.Flags[Data.Flag] = {
                Color = self.Color,
                HexValue =  self.HexValue,
                Alpha = self.Alpha
            }

            local ColorPositionX = MathClamp(1 - self.Saturation, 0, 0.989)
            local ColorPositionY = MathClamp(1 - self.Value, 0, 0.989)

            Items["PaletteDragger"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Position = UDim2New(ColorPositionX, 0, ColorPositionY, 0)})

            local HuePositionY = MathClamp(self.Hue, 0, 0.994)

            Items["HueDragger"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Position = UDim2New(0, 0, HuePositionY, 0)})

            local AlphaPositionX = MathClamp(self.Alpha, 0, 0.994)

            Items["AlphaDragger"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Position = UDim2New(AlphaPositionX, 0, 0, 0)})

            self:Update()
        end

        function Colorpicker:Update(IsFromAlpha)
            self.Color = FromHSV(self.Hue, self.Saturation, self.Value)
            self.HexValue = self.Color:ToHex()

            Library.Flags[Data.Flag] = {
                Color = self.Color,
                HexValue =  self.HexValue,
                Alpha = self.Alpha
            }

            Items["ColorpickerButton"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {BackgroundColor3 = self.Color})
            Items["Palette"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {BackgroundColor3 = FromHSV(self.Hue, 1, 1)})

            if not IsFromAlpha then 
                Items["Alpha"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {BackgroundColor3 = self.Color})
            end

            if Data.Callback then 
                Library:SafeCall(Data.Callback, self.Color, self.Alpha)
            end
        end

        function Colorpicker:SlidePalette(Input)
            if not Input or not SlidingPalette then 
                return
            end

            local ValueX = MathClamp(1 - (Input.Position.X - Items["Palette"].Instance.AbsolutePosition.X) / Items["Palette"].Instance.AbsoluteSize.X, 0, 1)
            local ValueY = MathClamp(1 - (Input.Position.Y - Items["Palette"].Instance.AbsolutePosition.Y) / Items["Palette"].Instance.AbsoluteSize.Y, 0, 1)

            self.Saturation = ValueX
            self.Value = ValueY

            local SlideX = MathClamp((Input.Position.X - Items["Palette"].Instance.AbsolutePosition.X) / Items["Palette"].Instance.AbsoluteSize.X, 0, 0.989)
            local SlideY = MathClamp((Input.Position.Y - Items["Palette"].Instance.AbsolutePosition.Y) / Items["Palette"].Instance.AbsoluteSize.Y, 0, 0.989)

            Items["PaletteDragger"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Position = UDim2New(SlideX, 0, SlideY, 0)})
            self:Update()            
        end

        function Colorpicker:SlideHue(Input)
            if not Input or not SlidingHue then 
                return
            end

            local ValueY = MathClamp((Input.Position.Y - Items["Hue"].Instance.AbsolutePosition.Y) / Items["Hue"].Instance.AbsoluteSize.Y, 0, 1)

            self.Hue = ValueY

            local PositionY = MathClamp((Input.Position.Y - Items["Hue"].Instance.AbsolutePosition.Y) / Items["Hue"].Instance.AbsoluteSize.Y, 0, 0.994)

            Items["HueDragger"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Position = UDim2New(0, 0, PositionY, 0)})
            self:Update()
        end

        function Colorpicker:SlideAlpha(Input)
            if not Input or not SlidingAlpha then 
                return
            end

            local ValueX = MathClamp((Input.Position.X - Items["Alpha"].Instance.AbsolutePosition.X) / Items["Alpha"].Instance.AbsoluteSize.X, 0, 1)
            
            self.Alpha = ValueX

            local PositionX = MathClamp((Input.Position.X - Items["Alpha"].Instance.AbsolutePosition.X) / Items["Alpha"].Instance.AbsoluteSize.X, 0, 0.994)

            Items["AlphaDragger"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Position = UDim2New(PositionX, 0, 0, 0)})
            self:Update(true)
        end

        Items["ColorpickerButton"]:Connect("MouseButton1Down", function()
            Colorpicker:SetOpen(not Colorpicker.IsOpen)
        end)

        Items["Palette"]:Connect("InputBegan", function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                SlidingPalette = true
                Colorpicker:SlidePalette(Input)
            end
        end)

        Items["Palette"]:Connect("InputEnded", function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                SlidingPalette = false
            end
        end)

        Items["Hue"]:Connect("InputBegan", function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                SlidingHue = true
                Colorpicker:SlideHue(Input)
            end
        end)

        Items["Hue"]:Connect("InputEnded", function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                SlidingHue = false
            end
        end)

        Items["Alpha"]:Connect("InputBegan", function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                SlidingAlpha = true
                Colorpicker:SlideAlpha(Input)
            end
        end)

        Items["Alpha"]:Connect("InputEnded", function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                SlidingAlpha = false
            end
        end)

        Library:Connect(UserInputService.InputChanged, function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseMovement then
                if SlidingPalette then
                    Colorpicker:SlidePalette(Input)
                end

                if SlidingHue then
                    Colorpicker:SlideHue(Input)
                end

                if SlidingAlpha then
                    Colorpicker:SlideAlpha(Input)
                end
            end
        end)

        Library:Connect(UserInputService.InputBegan, function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                if Library:IsMouseOverFrame(Items["ColorpickerWindow"]) then
                    return
                end

                Colorpicker:SetOpen(false)
            end
        end)

        if Data.Default then 
            Colorpicker:Set(Data.Default, Data.Alpha)
        end

        Library.SetFlags[Data.Flag] = function(Color, Alpha)
            Colorpicker:Set(Color, Alpha)
        end

        return Colorpicker
    end

    Library.CreateKeybind = function(self, Data)
        local Keybind = {
            Key = nil,
            Value = "",
            Mode = "",

            Toggled = false,
            IsOpen = false,

            Picking = false,

            Class = "Keybind"
        }

        Library.Flags[Data.Flag] = { }

        local KeyListItem

        local Items = { } do 
            Items["KeyButton"] = Instances:Create("TextButton", {
                Parent = Data.Parent.Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(27, 27, 32),
                Text = "",
                AutoButtonColor = false,
                AnchorPoint = Vector2New(1, 0),
                Size = UDim2New(0, 0, 1, 1),
                Name = "\0",
                Position = UDim2New(1, 0, 0, 0),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.X,
                TextSize = 14,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["KeyButton"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Outline"})

            if Library.KeyList then 
                KeyListItem = Library.KeyList:Add(Keybind.Mode, Data.Name, Keybind.Value)
            end
            
            Instances:Create("UIStroke", {
                Parent = Items["KeyButton"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(10, 10, 10)
            }):AddToTheme({Color = "Border"})
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["KeyButton"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "MB2",
                Name = "\0",
                BackgroundTransparency = 1,
                Position = UDim2New(0, 1, 0, 0),
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Instances:Create("UIPadding", {
                Parent = Items["KeyButton"].Instance,
                PaddingRight = UDimNew(0, 3),
                PaddingLeft = UDimNew(0, 3),
                PaddingBottom = UDimNew(0, 2)
            })             

            Items["Window"] = Instances:Create("Frame", {
                Parent = Data.Parent.Instance,
                BorderColor3 = FromRGB(10, 10, 10),
                AnchorPoint = Vector2New(1, 0),
                Name = "\0",
                Position = UDim2New(1, 0, 1, 5),
                Size = UDim2New(0, 50, 0, 48),
                BorderSizePixel = 2,
                Visible = false,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["Window"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Window"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["Toggle"] = Instances:Create("TextButton", {
                Parent = Items["Window"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(235, 157, 255),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "Toggle",
                AutoButtonColor = false,
                Name = "\0",
                BorderSizePixel = 0,
                BackgroundTransparency = 1,
                Position = UDim2New(0, 1, 0, 0),
                Size = UDim2New(1, 0, 0, 15),
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Toggle"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Toggle"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Hold"] = Instances:Create("TextButton", {
                Parent = Items["Window"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "Hold",
                AutoButtonColor = false,
                Name = "\0",
                BorderSizePixel = 0,
                BackgroundTransparency = 1,
                Position = UDim2New(0, 1, 0, 15),
                Size = UDim2New(1, 0, 0, 15),
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Hold"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Hold"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Always"] = Instances:Create("TextButton", {
                Parent = Items["Window"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "Always",
                AutoButtonColor = false,
                Name = "\0",
                BorderSizePixel = 0,
                BackgroundTransparency = 1,
                Position = UDim2New(0, 1, 0, 30),
                Size = UDim2New(1, 0, 0, 15),
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Always"]:AddToTheme({TextColor3 = "Text"})
             
            Instances:Create("UIStroke", {
                Parent = Items["Always"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
        end

        local Modes = {
            ["Toggle"] = Items["Toggle"],
            ["Hold"] = Items["Hold"],
            ["Always"] = Items["Always"]
        }

        local Update = function()
            if KeyListItem then
                KeyListItem:Set(Keybind.Mode, Data.Name, Keybind.Value)
                KeyListItem:SetStatus(Keybind.Toggled and "Active" or "Inactive")
            end
        end

        function Keybind:Get()
           return Keybind.Toggled, Keybind.Key, Keybind.Mode 
        end

        function Keybind:SetVisibility(Bool)
            Data.Parent.Instance.Visible = Bool
        end

        local Debounce = false

        function Keybind:SetOpen(Bool)
            Keybind.IsOpen = Bool

            if Bool then 
                Debounce = true
                Items["Window"].Instance.Visible = true
                Items["Window"].Instance.ZIndex = 16
                Items["Window"]:Tween(nil, {BackgroundTransparency = 0})

                task.wait(0.1)

                for Index, Value in Items["Window"].Instance:GetDescendants() do 
                    if Value:IsA("UIStroke") then
                        Tween:Create(Value, nil, {Transparency = 0}, true)
                    elseif Value:IsA("TextButton") then
                        Tween:Create(Value, nil, {TextTransparency = 0}, true)
                        Value.ZIndex = 16
                    end
                end
            else 
                for Index, Value in Items["Window"].Instance:GetDescendants() do 
                    if Value:IsA("UIStroke") then
                        Tween:Create(Value, nil, {Transparency = 1}, true)
                    elseif Value:IsA("TextButton") then
                        Tween:Create(Value, nil, {TextTransparency = 1}, true)
                        Value.ZIndex = 1
                    end
                end

                task.wait(0.1)

                Items["Window"]:Tween(nil, {BackgroundTransparency = 1})
                Items["Window"].Instance.ZIndex = 1
                task.wait(0.1)
                Items["Window"].Instance.Visible = false
            end

            Debounce = false
        end

        function Keybind:Set(Key)
            if StringFind(tostring(Key), "Enum") then 
                Keybind.Key = tostring(Key)

                Key = Key.Name == "Backspace" and "None" or Key.Name

                local KeyString = Keys[Keybind.Key] or StringGSub(Key, "Enum.", "") or "None"
                local TextToDisplay = StringGSub(StringGSub(KeyString, "KeyCode.", ""), "UserInputType.", "") or "None"

                Keybind.Value = TextToDisplay
                Items["Text"].Instance.Text = TextToDisplay
    
                if Data.Callback then 
                    Library:SafeCall(Data.Callback, Keybind.Toggled)
                end
           elseif TableFind({"Toggle", "Hold", "Always"}, Key) then 
                Keybind.Mode = Key
                
                Keybind:SetMode(Key)

                if Data.Callback then 
                    Library:SafeCall(Data.Callback, Keybind.Toggled)
                end
            elseif type(Key) == "table" then 
                local RealKey = Key.Key == "Backspace" and "None" or Key.Key
                Keybind.Key = tostring(Key.Key)

                if Key.Mode then
                    Keybind.Mode = Key.Mode
                    Keybind:SetMode(Key.Mode)
                else
                    Keybind.Mode = "Toggle"
                    Keybind:SetMode("Toggle")
                end

                local KeyString = Keys[Keybind.Key] or StringGSub(tostring(RealKey), "Enum.", "") or RealKey
                local TextToDisplay = KeyString and StringGSub(StringGSub(KeyString, "KeyCode.", ""), "UserInputType.", "") or "None"

                TextToDisplay = StringGSub(StringGSub(KeyString, "KeyCode.", ""), "UserInputType.", "")

                Keybind.Value = TextToDisplay
                Items["Text"].Instance.Text = TextToDisplay

                if Keybind.Callback then 
                    Library:SafeCall(Keybind.Callback, Keybind.Toggled)
                end
            end

            Keybind.Picking = false
            Items["Text"]:Tween(nil, {TextColor3 = Library.Theme.Text})
            Items["Text"]:ChangeItemTheme({TextColor3 = "Text"})
            Items["Text"].Instance.Size = UDim2New(0, Items["Text"].Instance.TextBounds.X, 1, 1)
            Update()
        end

        function Keybind:SetMode(Mode)
            for Index, Value in Modes do 
                if Index == Mode then 
                    Value:Tween(nil, {TextColor3 = Library.Theme.Accent})
                    Value:ChangeItemTheme({TextColor3 = "Accent"})
                else
                    Value:Tween(nil, {TextColor3 = Library.Theme.Text})
                    Value:ChangeItemTheme({TextColor3 = "Text"})
                end
            end

            if Keybind.Mode == "Always" then 
                Keybind.Toggled = true
            else
                Keybind.Toggled = false
            end

            Library.Flags[Data.Flag] = {
                Mode = Keybind.Mode,
                Key = Keybind.Key,
                Toggled = Keybind.Toggled
            }

            if Data.Callback then 
                Library:SafeCall(Data.Callback, Keybind.Toggled)
            end

            Update()
        end

        function Keybind:Press(Bool)
            if Keybind.Mode == "Toggle" then
                Keybind.Toggled = not Keybind.Toggled
            elseif Keybind.Mode == "Hold" then
                Keybind.Toggled = Bool
            elseif Keybind.Mode == "Always" then
                Keybind.Toggled = true
            end

            Library.Flags[Data.Flag] = {
                Mode = Keybind.Mode,
                Key = Keybind.Key,
                Toggled = Keybind.Toggled
            }

            if Data.Callback then 
                Library:SafeCall(Data.Callback, Keybind.Toggled)
            end

            Update()
        end

        Items["KeyButton"]:Connect("MouseButton1Click", function()
            if Keybind.Picking then 
                return
            end

            Keybind.Picking = true

            Items["Text"]:Tween(nil, {TextColor3 = Library.Theme.Accent})
            Items["Text"]:ChangeItemTheme({TextColor3 = "Accent"})

            local InputBegan 
            InputBegan = UserInputService.InputBegan:Connect(function(Input)
                if Input.UserInputType == Enum.UserInputType.Keyboard then 
                    Keybind:Set(Input.KeyCode)
                else
                    Keybind:Set(Input.UserInputType)
                end

                InputBegan:Disconnect()
                InputBegan = nil
            end)
        end)

        Items["KeyButton"]:Connect("MouseButton2Down", function()
            Keybind:SetOpen(not Keybind.IsOpen)
        end)

        Library:Connect(UserInputService.InputBegan, function(Input)
            if tostring(Input.KeyCode) == Keybind.Key or tostring(Input.UserInputType) == Keybind.Key then
                if Keybind.Mode == "Toggle" then 
                    Keybind:Press()
                elseif Keybind.Mode == "Hold" then 
                    Keybind:Press(true)
                end
            end

            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                if Library:IsMouseOverFrame(Items["Window"]) then
                    return
                end

                if Debounce then 
                    return
                end

                Keybind:SetOpen(false)
            end
        end)

        Library:Connect(UserInputService.InputEnded, function(Input)
            if tostring(Input.KeyCode) == Keybind.Key or tostring(Input.UserInputType) == Keybind.Key then
                if Keybind.Mode == "Hold" then 
                    Keybind:Press(false)
                end
            end
        end)

        Items["Toggle"]:Connect("MouseButton1Down", function()
            Keybind.Mode = "Toggle"
            Keybind:SetMode("Toggle")
        end)

        Items["Always"]:Connect("MouseButton1Down", function()
            Keybind.Mode = "Always"
            Keybind:SetMode("Always")
        end)

        Items["Hold"]:Connect("MouseButton1Down", function()
            Keybind.Mode = "Hold"
            Keybind:SetMode("Hold")
        end)

        if Data.Default then 
            Keybind:Set({
                Key = Data.Default,
                Mode = Data.Mode or "Toggle"
            })
        end

        Library.SetFlags[Data.Flag] = function(Value)
            Keybind:Set(Value)
        end

        return Keybind
    end

    Library.Window = function(self, Data)
        Data = Data or { }

        local Window = {
            Name = Data.Name or Data.name or "Window",
            Size = Data.Size or Data.size or UDim2New(0, 500, 0, 600),

            FadeSpeed = Data.FadeSpeed or Data.fadespeed or 0.25,

            Pages = { },
            SubPages = { },
            Elements = { },

            IsOpen = true
        }

        local Items = { } do 
            Items["MainFrame"] = Instances:Create("Frame", {
                Parent = Library.Holder.Instance,
                AnchorPoint = Vector2New(0, 0),
                Name = "\0",
                Position = UDim2New(0, 0, 0, 0),
                BorderColor3 = FromRGB(10, 10, 10),
                Size = Window.Size,
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["MainFrame"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})

            Items["MainFrame"].Instance.Position = UDim2New(0, Camera.ViewportSize.X / 4, 0, Camera.ViewportSize.Y / 4)

            Items["MainFrame"]:MakeDraggable()
            Items["MainFrame"]:MakeResizeable(Vector2New(Window.Size.X.Offset, Window.Size.Y.Offset), Vector2New(9999, 9999))
            
            Items["AccentBorder"] = Instances:Create("UIStroke", {
                Parent = Items["MainFrame"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(235, 157, 255)
            })  Items["AccentBorder"]:AddToTheme({Color = "Accent"})
            
            Items["Title"] = Instances:Create("TextLabel", {
                Parent = Items["MainFrame"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Window.Name,
                Name = "\0",
                Size = UDim2New(1, 0, 0, 15),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Position = UDim2New(0, 6, 0, 1),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Title"]:AddToTheme({TextColor3 = "Text"})

            Instances:Create("UIStroke", {
                Parent = Items["Title"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Inline"] = Instances:Create("Frame", {
                Parent = Items["MainFrame"].Instance,
                Name = "\0",
                Position = UDim2New(0, 7, 0, 20),
                BorderColor3 = FromRGB(27, 27, 32),
                Size = UDim2New(1, -14, 1, -27),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(20, 20, 25)
            })  Items["Inline"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Outline"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Inline"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                Color = Library.Theme.Border,
                Name = "\0"
            }):AddToTheme({Color = "Border"})
            
            Items["Pages"] = Instances:Create("Frame", {
                Parent = Items["Inline"].Instance,
                Name = "\0",
                BackgroundTransparency = 1,
                Position = UDim2New(0, 7, 0, 7),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, -14, 0, 19),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })
            
            Instances:Create("UIListLayout", {
                Parent = Items["Pages"].Instance,
                FillDirection = Enum.FillDirection.Horizontal,
                HorizontalFlex = Enum.UIFlexAlignment.Fill,
                Padding = UDimNew(0, 6),
                SortOrder = Enum.SortOrder.LayoutOrder
            })

            Items["Content"] = Instances:Create("Frame", {
                Parent = Items["Inline"].Instance,
                Name = "\0",
                Position = UDim2New(0, 7, 0, 26),
                BorderColor3 = FromRGB(10, 10, 10),
                Size = UDim2New(1, -14, 1, -33),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["Content"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})
        
            Instances:Create("UIStroke", {
                Parent = Items["Content"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                Color = Library.Theme.Outline,
                Name = "\0"
            }):AddToTheme({Color = "Outline"})
        end

        local Debounce = false

        function Window:SetOpen(Bool)
            if Debounce then 
                return 
            end

            Window.IsOpen = Bool

            Debounce = true 

            if Bool then 
                Items["MainFrame"].Instance.Visible = true
            end

            local Descendants = Items["MainFrame"].Instance:GetDescendants()
            TableInsert(Descendants, Items["MainFrame"].Instance)

            local NewTween
            for Index, Value in Descendants do 
                local ValueIndex = Library:GetTransparencyPropertyFromItem(Value)

                if not ValueIndex then 
                    continue
                end

                if type(ValueIndex) == "table" then
                    for _, Property in ValueIndex do 
                        NewTween = Library:FadeItem(Value, Property, Bool, Window.FadeSpeed)
                    end
                else
                    NewTween = Library:FadeItem(Value, ValueIndex, Bool, Window.FadeSpeed)
                end
            end

            Library:Connect(NewTween.Tween.Completed, function()
                Debounce = false
                Items["MainFrame"].Instance.Visible = Bool
            end)
        end

        Library:Connect(UserInputService.InputBegan, function(Input)
            if tostring(Input.KeyCode) == Library.MenuKeybind or tostring(Input.UserInputType) == Library.MenuKeybind then
                Window:SetOpen(not Window.IsOpen)
            end
        end)

        Window.Elements = Items

        return setmetatable(Window, Library)
    end

    Library.Page = function(self, Data)
        Data = Data or { }

        local Page = {
            Window = self,

            Name = Data.Name or Data.name or "Page",
            Columns = Data.Columns or Data.columns or 2,

            HasSubtabs = Data.Subtabs or Data.subtabs or false,

            Active = false,
            ColumnsData = { },
            Elements = { }
        }

        local Items = { } do 
            Items["Inactive"] = Instances:Create("TextButton", {
                Parent = Page.Window.Elements["Pages"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(10, 10, 10),
                Text = "",
                AutoButtonColor = false,
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 2,
                TextSize = 14,
                BackgroundColor3 = FromRGB(30, 30, 35)
            })  Items["Inactive"]:AddToTheme({BackgroundColor3 = "Page Background", BorderColor3 = "Border"})

            Instances:Create("UIStroke", {
                Parent = Items["Inactive"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                Color = Library.Theme.Outline,
                Name = "\0"
            }):AddToTheme({Color = "Outline"})
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Inactive"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                TextTransparency = 0.47999998927116394,
                Text = Page.Name,
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BackgroundTransparency = 1,
                Position = UDim2New(0, 0, 0, -1),
                BorderSizePixel = 0,
                BorderColor3 = FromRGB(0, 0, 0),
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Hide"] = Instances:Create("Frame", {
                Parent = Items["Inactive"].Instance,
                Visible = false,
                BorderColor3 = FromRGB(0, 0, 0),
                AnchorPoint = Vector2New(0, 1),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 0),
                Size = UDim2New(1, 0, 0, 3),
                ZIndex = 2,
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["Hide"]:AddToTheme({BackgroundColor3 = "Background"})
            
            Items["MiscPixel1"] = Instances:Create("Frame", {
                Parent = Items["Hide"].Instance,
                Size = UDim2New(0, 1, 0, 1),
                Name = "\0",
                Position = UDim2New(0, -1, 0, 1),
                BorderColor3 = FromRGB(0, 0, 0),
                ZIndex = 2,
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(27, 27, 32)
            })  Items["MiscPixel1"]:AddToTheme({BackgroundColor3 = "Outline"})
            
            Items["MiscPixel2"] = Instances:Create("Frame", {
                Parent = Items["Hide"].Instance,
                BorderColor3 = FromRGB(0, 0, 0),
                AnchorPoint = Vector2New(1, 0),
                Name = "\0",
                Position = UDim2New(1, 1, 0, 1),
                Size = UDim2New(0, 1, 0, 1),
                ZIndex = 2,
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(27, 27, 32)
            })  Items["MiscPixel2"]:AddToTheme({BackgroundColor3 = "Outline"})
            
            Items["UIGradient"] = Instances:Create("UIGradient", {
                Parent = Items["Inactive"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(108, 108, 108))}
            })            

            Items["Page"] = Instances:Create("Frame", {
                Parent = Page.Window.Elements["Content"].Instance,
                BackgroundTransparency = 1,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255),
                Visible = false
            })
            
            if not Page.HasSubtabs then 
                Instances:Create("UIListLayout", {
                    Parent = Items["Page"].Instance,
                    FillDirection = Enum.FillDirection.Horizontal,
                    HorizontalFlex = Enum.UIFlexAlignment.Fill,
                    SortOrder = Enum.SortOrder.LayoutOrder,
                    VerticalFlex = Enum.UIFlexAlignment.Fill
                })
                
                for Index = 1, Page.Columns do
                    local NewColumn = Instances:Create("ScrollingFrame", {
                        Parent = Items["Page"].Instance,
                        ScrollBarImageColor3 = FromRGB(235, 157, 255),
                        Active = true,
                        AutomaticCanvasSize = Enum.AutomaticSize.Y,
                        ScrollBarThickness = 1,
                        Name = "\0",
                        BackgroundTransparency = 1,
                        Size = UDim2New(0, 100, 0, 100),
                        BackgroundColor3 = FromRGB(255, 255, 255),
                        BorderColor3 = FromRGB(0, 0, 0),
                        BorderSizePixel = 0,
                        BottomImage = Library:GetImage("Scrollbar"),
                        MidImage = Library:GetImage("Scrollbar"),
                        TopImage = Library:GetImage("Scrollbar"),
                        CanvasSize = UDim2New(0, 0, 0, 0)
                    })  NewColumn:AddToTheme({ScrollBarImageColor3 = "Accent"})
                    
                    Instances:Create("UIPadding", {
                        Parent = NewColumn.Instance,
                        PaddingTop = UDimNew(0, 6),
                        PaddingBottom = UDimNew(0, 6),
                        PaddingRight = UDimNew(0, 6),
                        PaddingLeft = UDimNew(0, 6)
                    })
                    
                    Instances:Create("UIListLayout", {
                        Parent = NewColumn.Instance,
                        Padding = UDimNew(0, 8),
                        SortOrder = Enum.SortOrder.LayoutOrder
                    }) 

                    Page.ColumnsData[Index] = NewColumn
                end
            else
                Items["Columns"] = Instances:Create("Frame", {
                    Parent = Items["Page"].Instance,
                    Name = "\0",
                    Position = UDim2New(0, 7, 0, 45),
                    BorderColor3 = FromRGB(10, 10, 10),
                    Size = UDim2New(1, -14, 1, -52),
                    BorderSizePixel = 2,
                    BackgroundColor3 = FromRGB(15, 15, 20)
                })  Items["Columns"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})

                Items["SubTabs"] = Instances:Create("Frame", {
                    Parent = Items["Page"].Instance,
                    Name = "\0",
                    BackgroundTransparency = 1,
                    Position = UDim2New(0, 7, 0, 7),
                    BorderColor3 = FromRGB(0, 0, 0),
                    Size = UDim2New(1, -14, 0, 35),
                    BorderSizePixel = 0,
                    BackgroundColor3 = FromRGB(255, 255, 255)
                }) 

                Instances:Create("UIListLayout", {
                    Parent = Items["SubTabs"].Instance,
                    FillDirection = Enum.FillDirection.Horizontal,
                    HorizontalFlex = Enum.UIFlexAlignment.Fill,
                    Padding = UDimNew(0, 6),
                    SortOrder = Enum.SortOrder.LayoutOrder
                }) 
            end
        end

        local Debounce = false

        function Page:Turn(Bool)
            if Debounce then 
                return 
            end

            Page.Active = Bool

            Debounce = true 

            if Bool then 
                Items["Page"].Instance.Visible = true

                Items["Text"]:Tween(nil, {TextColor3 = Library.Theme.Accent, TextTransparency = 0})
                Items["Hide"].Instance.Visible = true

                Items["Text"]:ChangeItemTheme({TextColor3 = "Accent"})
            else
                Items["Text"]:Tween(nil, {TextColor3 = Library.Theme.Text, TextTransparency = 0.5})
                Items["Hide"].Instance.Visible = false

                Items["Text"]:ChangeItemTheme({TextColor3 = "Text"})
            end

            local Descendants = Items["Page"].Instance:GetDescendants()
            TableInsert(Descendants, Items["Page"].Instance)

            local NewTween
            for Index, Value in Descendants do 
                local ValueIndex = Library:GetTransparencyPropertyFromItem(Value)

                if not ValueIndex then 
                    continue
                end

                if type(ValueIndex) == "table" then
                    for _, Property in ValueIndex do 
                        NewTween = Library:FadeItem(Value, Property, Bool, Page.Window.FadeSpeed or 0.5)
                    end
                else
                    NewTween = Library:FadeItem(Value, ValueIndex, Bool, Page.Window.FadeSpeed or 0.5)
                end
            end

            Library:Connect(NewTween.Tween.Completed, function()
                Debounce = false
                Items["Page"].Instance.Visible = Bool
            end)
        end

        Items["Inactive"]:Connect("MouseButton1Down", function()
            for Index, Value in Page.Window.Pages do
                Value:Turn(Value == Page)
            end
        end)

        if #Page.Window.Pages == 0 then 
            Page:Turn(true)
        end

        Page.Elements = Items

        TableInsert(Page.Window.Pages, Page)
        return setmetatable(Page, Library.Pages)
    end

    Library.Pages.SubPage = function(self, Data)
        Data = Data or { }

        local SubPage = {
            Window = self.Window,
            Page = self,

            Icon = Data.Icon or Data.icon or "9080568477801",
            Columns = Data.Columns or Data.columns or 2,

            Active = false,
            ColumnsData = { },
            Elements = { }
        }

        local Items = { } do
            Items["Inactive"] = Instances:Create("TextButton", {
                Parent = SubPage.Page.Elements["SubTabs"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(10, 10, 10),
                Text = "",
                AutoButtonColor = false,
                Name = "\0",
                Size = UDim2New(1, 0, 1, -2),
                BorderSizePixel = 2,
                TextSize = 14,
                BackgroundColor3 = FromRGB(30, 30, 35)
            })  Items["Inactive"]:AddToTheme({BackgroundColor3 = "Page Background", BorderColor3 = "Border"})

            Instances:Create("UIStroke", {
                Parent = Items["Inactive"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})

            Items["Hide"] = Instances:Create("Frame", {
                Parent = Items["Inactive"].Instance,
                Visible = false,
                BorderColor3 = FromRGB(0, 0, 0),
                AnchorPoint = Vector2New(0, 1),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 2),
                Size = UDim2New(1, 0, 0, 2),
                ZIndex = 5,
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(20, 20, 25)
            })  Items["Hide"]:AddToTheme({BackgroundColor3 = "Background"})

            Items["MiscPixel1"] = Instances:Create("Frame", {
                Parent = Items["Hide"].Instance,
                Size = UDim2New(0, 1, 0, 1),
                Name = "\0",
                Position = UDim2New(0, -1, 0, 1),
                BorderColor3 = FromRGB(0, 0, 0),
                ZIndex = 5,
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(27, 27, 32)
            }) 

            Items["MiscPixel2"] = Instances:Create("Frame", {
                Parent = Items["Hide"].Instance,
                BorderColor3 = FromRGB(0, 0, 0),
                AnchorPoint = Vector2New(1, 0),
                Name = "\0",
                Position = UDim2New(1, 1, 0, 1),
                Size = UDim2New(0, 1, 0, 1),
                ZIndex = 5,
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(27, 27, 32)
            }) 

            Items["Icon"] = Instances:Create("ImageLabel", {
                Parent = Items["Inactive"].Instance,
                ScaleType = Enum.ScaleType.Fit,
                ImageTransparency = 0.35,
                BorderColor3 = FromRGB(0, 0, 0),
                Name = "\0",
                AnchorPoint = Vector2New(0.5, 0.5),
                Image = "rbxassetid://"..SubPage.Icon,
                BackgroundTransparency = 1,
                Position = UDim2New(0.5, 0, 0.5, 0),
                Size = UDim2New(0, 30, 0, 30),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Icon"]:AddToTheme({ImageColor3 = "Text"})

            Instances:Create("UIGradient", {
                Parent = Items["Inactive"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(138, 138, 138))}
            }) 

            Items["Subtab"] = Instances:Create("Frame", {
                Parent = SubPage.Page.Elements["Columns"].Instance,
                BackgroundTransparency = 1,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 

            Instances:Create("UIPadding", {
                Parent = Items["Subtab"].Instance,
                PaddingTop = UDimNew(0, 6),
                PaddingRight = UDimNew(0, 6),
                PaddingLeft = UDimNew(0, 6)
            }) 

            Instances:Create("UIListLayout", {
                Parent = Items["Subtab"].Instance,
                FillDirection = Enum.FillDirection.Horizontal,
                HorizontalFlex = Enum.UIFlexAlignment.Fill,
                SortOrder = Enum.SortOrder.LayoutOrder,
                VerticalFlex = Enum.UIFlexAlignment.Fill
            }) 

            Instances:Create("UIStroke", {
                Parent = Items["Subtab"].Instance,
                Color = FromRGB(27, 27, 32),
                Name = "\0",
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border
            }):AddToTheme({Color = "Outline"})

            for Index = 1, SubPage.Columns do
                local NewColumn = Instances:Create("ScrollingFrame", {
                    Parent = Items["Subtab"].Instance,
                    ScrollBarImageColor3 = FromRGB(235, 157, 255),
                    Active = true,
                    AutomaticCanvasSize = Enum.AutomaticSize.Y,
                    ScrollBarThickness = 1,
                    Name = "\0",
                    BackgroundTransparency = 1,
                    Size = UDim2New(0, 100, 0, 100),
                    BackgroundColor3 = FromRGB(255, 255, 255),
                    BorderColor3 = FromRGB(0, 0, 0),
                    BorderSizePixel = 0,
                    CanvasSize = UDim2New(0, 0, 0, 0)
                })  NewColumn:AddToTheme({ScrollBarImageColor3 = "Accent"})

                Instances:Create("UIPadding", {
                    Parent = NewColumn.Instance,
                    PaddingTop = UDimNew(0, 6),
                    PaddingBottom = UDimNew(0, 6),
                    PaddingRight = UDimNew(0, 6),
                    PaddingLeft = UDimNew(0, 6)
                }) 

                Instances:Create("UIListLayout", {
                    Parent = NewColumn.Instance,
                    Padding = UDimNew(0, 8),
                    SortOrder = Enum.SortOrder.LayoutOrder
                }) 

                SubPage.ColumnsData[Index] = NewColumn
            end
        end

        local Debounce = false

        function SubPage:Turn(Bool)
            if Debounce then 
                return 
            end

            SubPage.Active = Bool

            Debounce = true 

            if Bool then 
                Items["Subtab"].Instance.Visible = true

                Items["Icon"]:Tween(nil, {ImageColor3 = Library.Theme.Accent, ImageTransparency = 0})
                Items["Hide"].Instance.Visible = true

                Items["Icon"]:ChangeItemTheme({ImageColor3 = "Accent"})

                Items["Inactive"].Instance.Size = UDim2New(1, 0, 1, 1)
            else
                Items["Icon"]:Tween(nil, {ImageColor3 = Library.Theme.Text, ImageTransparency = 0.35})
                Items["Hide"].Instance.Visible = false

                Items["Icon"]:ChangeItemTheme({ImageColor3 = "Text"})
                Items["Inactive"].Instance.Size = UDim2New(1, 0, 1, -2)
            end

            local Descendants = Items["Subtab"].Instance:GetDescendants()
            TableInsert(Descendants, Items["Subtab"].Instance)

            local NewTween
            for Index, Value in Descendants do 
                local ValueIndex = Library:GetTransparencyPropertyFromItem(Value)

                if not ValueIndex then 
                    continue
                end

                if type(ValueIndex) == "table" then
                    for _, Property in ValueIndex do 
                        NewTween = Library:FadeItem(Value, Property, Bool, SubPage.Window.FadeSpeed or 0.5)
                    end
                else
                    NewTween = Library:FadeItem(Value, ValueIndex, Bool, SubPage.Window.FadeSpeed or 0.5)
                end
            end

            Library:Connect(NewTween.Tween.Completed, function()
                Debounce = false
                Items["Subtab"].Instance.Visible = Bool
            end)
        end

        Items["Inactive"]:Connect("MouseButton1Down", function()
            for Index, Value in SubPage.Window.SubPages do
                Value:Turn(Value == SubPage)
            end
        end)

        if #SubPage.Window.SubPages == 0 then 
            SubPage:Turn(true)
        end

        SubPage.Elements = Items

        TableInsert(SubPage.Window.SubPages, SubPage)
        return setmetatable(SubPage, Library.Pages)
    end

    Library.Pages.Section = function(self, Data)
        Data = Data or { }

        local Section = {
            Window = self.Window,
            Page = self,

            Name = Data.Name or Data.name or "Section",
            Side = Data.Side or Data.side or 1,

            Elements = { }
        }

        local Items = { } do 
            Items["Section"] = Instances:Create("Frame", {
                Parent = Section.Page.ColumnsData[Section.Side].Instance,
                Name = "\0",
                Size = UDim2New(1, 0, 0, 25),
                BorderColor3 = FromRGB(27, 27, 32),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.Y,
                BackgroundColor3 = FromRGB(20, 20, 25)
            })  Items["Section"]:AddToTheme({BackgroundColor3 = "Inline", BorderColor3 = "Outline"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Section"].Instance,
                Color = FromRGB(10, 10, 10),
                Name = "\0",
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border
            }):AddToTheme({Color = "Border"})
            
            Instances:Create("UIPadding", {
                Parent = Items["Section"].Instance,
                PaddingBottom = UDimNew(0, 6)
            })
            
            Items["AccentLine"] = Instances:Create("Frame", {
                Parent = Items["Section"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(235, 157, 255)
            })  Items["AccentLine"]:AddToTheme({BackgroundColor3 = "Accent"})
            
            Instances:Create("UIGradient", {
                Parent = Items["AccentLine"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(65, 65, 65))}
            })
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Section"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Section.Name,
                Name = "\0",
                Size = UDim2New(1, -12, 0, 15),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Position = UDim2New(0, 4, 0, 2),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Content"] = Instances:Create("Frame", {
                Parent = Items["Section"].Instance,
                Name = "\0",
                BackgroundTransparency = 1,
                Position = UDim2New(0, 7, 0, 21),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, -14, 1, -20),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })
            
            Instances:Create("UIListLayout", {
                Parent = Items["Content"].Instance,
                Padding = UDimNew(0, 6),
                SortOrder = Enum.SortOrder.LayoutOrder
            })
        end

        Section.Elements = Items

        return setmetatable(Section, Library.Sections)
    end

    Library.Pages.MultiSection = function(self, Data)
        local MultiSection = {
            Window = self.Window,
            Page = self,
            
            Sections = Data.Sections or Data.sections or { "Section 1", "Section 2", "Section 3" }, 
            Side = Data.Side or Data.side or 1,

            SectionContents = { },

            Elements = { }
        }

        local Items = { } do
            Items["MultiSection"] = Instances:Create("Frame", {
                Parent = MultiSection.Page.ColumnsData[MultiSection.Side].Instance,
                Name = "\0",
                Size = UDim2New(1, 0, 0, 25),
                BorderColor3 = FromRGB(27, 27, 32),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.Y,
                BackgroundColor3 = FromRGB(20, 20, 25)
            })  Items["MultiSection"]:AddToTheme({BackgroundColor3 = "Inline", BorderColor3 = "Outline"})
            
            Instances:Create("UIStroke", {
                Parent = Items["MultiSection"].Instance,
                Color = FromRGB(10, 10, 10),
                Name = "\0",
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border
            }):AddToTheme({Color = "Border"})
            
            Instances:Create("UIPadding", {
                Parent = Items["MultiSection"].Instance,
                PaddingBottom = UDimNew(0, 6)
            }) 
            
            Items["AccentLine"] = Instances:Create("Frame", {
                Parent = Items["MultiSection"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(235, 157, 255)
            })  Items["AccentLine"]:AddToTheme({BackgroundColor3 = "Accent"})
            
            Instances:Create("UIGradient", {
                Parent = Items["AccentLine"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(65, 65, 65))}
            }) 
            
            Items["Sections"] = Instances:Create("Frame", {
                Parent = Items["MultiSection"].Instance,
                Name = "\0",
                BackgroundTransparency = 1,
                Position = UDim2New(0, 7, 0, 9),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, -14, 0, 19),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Instances:Create("UIListLayout", {
                Parent = Items["Sections"].Instance,
                FillDirection = Enum.FillDirection.Horizontal,
                HorizontalFlex = Enum.UIFlexAlignment.Fill,
                Padding = UDimNew(0, 5),
                SortOrder = Enum.SortOrder.LayoutOrder
            }) 

            Items["Content"] = Instances:Create("Frame", {
                Parent = Items["MultiSection"].Instance,
                Name = "\0",
                BackgroundTransparency = 1,
                Position = UDim2New(0, 7, 0, 35),
                BorderColor3 = FromRGB(10, 10, 10),
                Size = UDim2New(1, -14, 1, -33),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(15, 15, 20)
            }) 
        end

        for Index, Value in MultiSection.Sections do 
            local NewSection = {
                Window = MultiSection.Window,
                Page = MultiSection.Page,
                MultiSection = MultiSection,

                Name = Value,

                Elements = { },

                Active = false,
            }

            local SubItems = { } do 
                SubItems["Inactive"] = Instances:Create("TextButton", {
                    Parent = Items["Sections"].Instance,
                    FontFace = Library.Font,
                    TextColor3 = FromRGB(0, 0, 0),
                    BorderColor3 = FromRGB(10, 10, 10),
                    Text = "",
                    AutoButtonColor = false,
                    Name = "\0",
                    Size = UDim2New(1, 0, 1, 0),
                    BorderSizePixel = 2,
                    TextSize = 14,
                    BackgroundColor3 = FromRGB(30, 30, 35)
                })  SubItems["Inactive"]:AddToTheme({BackgroundColor3 = "Page Background", BorderColor3 = "Border"})

                SubItems["Text"] = Instances:Create("TextLabel", {
                    Parent = SubItems["Inactive"].Instance,
                    FontFace = Library.Font,
                    TextColor3 = FromRGB(215, 215, 215),
                    TextTransparency = 0.48,
                    Text = NewSection.Name,
                    Name = "\0",
                    Size = UDim2New(1, 0, 1, 0),
                    BackgroundTransparency = 1,
                    Position = UDim2New(0, 0, 0, -1),
                    BorderSizePixel = 0,
                    BorderColor3 = FromRGB(0, 0, 0),
                    TextSize = 12,
                    BackgroundColor3 = FromRGB(255, 255, 255)
                })  SubItems["Text"]:AddToTheme({TextColor3 = "Text"})

                Instances:Create("UIStroke", {
                    Parent = SubItems["Text"].Instance,
                    LineJoinMode = Enum.LineJoinMode.Miter,
                    Name = "\0"
                }):AddToTheme({Color = "Text Border"})

                SubItems["Hide"] = Instances:Create("Frame", {
                    Parent = SubItems["Inactive"].Instance,
                    Visible = false,
                    BorderColor3 = FromRGB(0, 0, 0),
                    AnchorPoint = Vector2New(0, 1),
                    Name = "\0",
                    Position = UDim2New(0, 0, 1, 0),
                    Size = UDim2New(1, 0, 0, 3),
                    ZIndex = 2,
                    BorderSizePixel = 0,
                    BackgroundColor3 = FromRGB(15, 15, 20)
                })  SubItems["Hide"]:AddToTheme({BackgroundColor3 = "Background"})

                SubItems["MiscPixel1"] = Instances:Create("Frame", {
                    Parent = SubItems["Hide"].Instance,
                    Size = UDim2New(0, 1, 0, 1),
                    Name = "\0",
                    Position = UDim2New(0, -1, 0, 1),
                    BorderColor3 = FromRGB(0, 0, 0),
                    ZIndex = 2,
                    BorderSizePixel = 0,
                    BackgroundColor3 = FromRGB(27, 27, 32)
                })  SubItems["MiscPixel1"]:AddToTheme({BackgroundColor3 = "Outline"})

                SubItems["MiscPixel2"] = Instances:Create("Frame", {
                    Parent = SubItems["Hide"].Instance,
                    BorderColor3 = FromRGB(0, 0, 0),
                    AnchorPoint = Vector2New(1, 0),
                    Name = "\0",
                    Position = UDim2New(1, 1, 0, 1),
                    Size = UDim2New(0, 1, 0, 1),
                    ZIndex = 2,
                    BorderSizePixel = 0,
                    BackgroundColor3 = FromRGB(27, 27, 32)
                })  SubItems["MiscPixel2"]:AddToTheme({BackgroundColor3 = "Outline"})

                Instances:Create("UIStroke", {
                    Parent = SubItems["Inactive"].Instance,
                    ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                    LineJoinMode = Enum.LineJoinMode.Miter,
                    Name = "\0",
                    Color = FromRGB(27, 27, 32)
                }):AddToTheme({Color = "Outline"})

                Instances:Create("UIGradient", {
                    Parent = SubItems["Inactive"].Instance,
                    Rotation = 90,
                    Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(108, 108, 108))}
                }) 

                SubItems["Content"] = Instances:Create("Frame", {
                    Parent = Items["Content"].Instance,
                    BackgroundTransparency = 1,
                    Name = "\0",
                    BorderColor3 = FromRGB(0, 0, 0),
                    Size = UDim2New(1, 0, 1, 0),
                    BorderSizePixel = 0,
                    Visible = false,
                    BackgroundColor3 = FromRGB(255, 255, 255)
                }) 
                
                Instances:Create("UIListLayout", {
                    Parent = SubItems["Content"].Instance,
                    Padding = UDimNew(0, 6),
                    SortOrder = Enum.SortOrder.LayoutOrder
                }) 
            end

            local Debounce = false

            function NewSection:Turn(Bool)
                if Debounce then 
                    return 
                end

                NewSection.Active = Bool

                Debounce = true 

                if Bool then 
                    SubItems["Content"].Instance.Visible = true

                    SubItems["Text"]:Tween(nil, {TextColor3 = Library.Theme.Accent, TextTransparency = 0})

                    SubItems["Text"]:ChangeItemTheme({TextColor3 = "Accent"})
                else
                    SubItems["Text"]:Tween(nil, {TextColor3 = Library.Theme.Text, TextTransparency = 0.5})

                    SubItems["Text"]:ChangeItemTheme({TextColor3 = "Text"})
                end

                local Descendants = SubItems["Content"].Instance:GetDescendants()
                TableInsert(Descendants, SubItems["Content"].Instance)

                local NewTween
                for Index, Value in Descendants do 
                    local ValueIndex = Library:GetTransparencyPropertyFromItem(Value)

                    if not ValueIndex then 
                        continue
                    end

                    if type(ValueIndex) == "table" then
                        for _, Property in ValueIndex do 
                            NewTween = Library:FadeItem(Value, Property, Bool, MultiSection.Window.FadeSpeed or 0.5)
                        end
                    else
                        NewTween = Library:FadeItem(Value, ValueIndex, Bool, MultiSection.Window.FadeSpeed or 0.5)
                    end
                end

                Library:Connect(NewTween.Tween.Completed, function()
                    Debounce = false
                    SubItems["Content"].Instance.Visible = Bool
                end)
            end

            SubItems["Inactive"]:Connect("MouseButton1Down", function()
                for Index, Value in MultiSection.SectionContents do
                    Value:Turn(Value == NewSection)
                end
            end)

            if #MultiSection.SectionContents == 0 then 
                NewSection:Turn(true)
            end

            NewSection.Elements = SubItems

            MultiSection.SectionContents[#MultiSection.SectionContents+1] = setmetatable(NewSection, Library.Sections)
        end

        MultiSection.SectionContents[1]:Turn(true)
        MultiSection.Window.Sections[#MultiSection.Window.Sections+1] = MultiSection
        return TableUnpack(MultiSection.SectionContents)
    end

    Library.Pages.ScrollableSection = function(self, Data)
        Data = Data or { }

        local Section = {
            Window = self.Window,
            Page = self,

            Name = Data.Name or Data.name or "Section",
            Side = Data.Side or Data.side or 1,
            Size = Data.Size or Data.size or 175,

            Elements = { }
        }

        local Items = { } do 
            Items["Section"] = Instances:Create("Frame", {
                Parent = Section.Page.ColumnsData[Section.Side].Instance,
                Name = "\0",
                Size = UDim2New(1, 0, 0, Section.Size),
                BorderColor3 = FromRGB(27, 27, 32),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.Y,
                BackgroundColor3 = FromRGB(20, 20, 25)
            })  Items["Section"]:AddToTheme({BackgroundColor3 = "Inline", BorderColor3 = "Outline"})

            Items["Fade"] = Instances:Create("Frame", {
                Parent = Items["Section"].Instance,
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 20),
                AnchorPoint = Vector2New(0, 1),
                Position = UDim2New(0, 0, 1, 2),
                BorderSizePixel = 0,
                ZIndex = 15,
                BackgroundColor3 = FromRGB(27, 27, 32)
            })  Items["Fade"]:AddToTheme({BackgroundColor3 = "Inline"})

            Instances:Create("UIGradient", {
                Parent = Items["Fade"].Instance,
                Rotation = -90,
                Transparency = NumSequence{NumSequenceKeypoint(0, 0), NumSequenceKeypoint(0.718, 0.768750011920929), NumSequenceKeypoint(1, 1)}
            })
            
            Instances:Create("UIStroke", {
                Parent = Items["Section"].Instance,
                Color = FromRGB(10, 10, 10),
                Name = "\0",
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border
            }):AddToTheme({Color = "Border"})
            
            Instances:Create("UIPadding", {
                Parent = Items["Section"].Instance,
                PaddingBottom = UDimNew(0, 6)
            })
            
            Items["AccentLine"] = Instances:Create("Frame", {
                Parent = Items["Section"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 2),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(235, 157, 255)
            })  Items["AccentLine"]:AddToTheme({BackgroundColor3 = "Accent"})
            
            Instances:Create("UIGradient", {
                Parent = Items["AccentLine"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(65, 65, 65))}
            })
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Section"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Section.Name,
                Name = "\0",
                Size = UDim2New(1, -12, 0, 15),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Position = UDim2New(0, 4, 0, 2),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Content"] = Instances:Create("ScrollingFrame", {
                Parent = Items["Section"].Instance,
                Name = "\0",
                ScrollBarThickness = 3,
                AutomaticCanvasSize = Enum.AutomaticSize.Y,
                CanvasSize = UDim2New(0, 0, 0, 0),
                ScrollBarImageColor3 = FromRGB(235, 157, 255),
                MidImage = Library:GetImage("Scrollbar"),
                TopImage = Library:GetImage("Scrollbar"),
                BottomImage = Library:GetImage("Scrollbar"),
                Active = true,
                BackgroundTransparency = 1,
                Position = UDim2New(0, 0, 0, 21),
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, -5, 1, -20),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Content"]:AddToTheme({ScrollBarImageColor3 = "Accent"})

            Instances:Create("UIPadding", {
                Parent = Items["Content"].Instance,
                PaddingTop = UDimNew(0, 0),
                PaddingBottom = UDimNew(0, 8),
                PaddingRight = UDimNew(0, 11),
                PaddingLeft = UDimNew(0, 8)
            })
            
            Instances:Create("UIListLayout", {
                Parent = Items["Content"].Instance,
                Padding = UDimNew(0, 6),
                SortOrder = Enum.SortOrder.LayoutOrder
            })
        end

        Section.Elements = Items

        return setmetatable(Section, Library.Sections)
    end

    Library.Sections.Divider = function(self)
        local Divider = {
            Window = self.Window,
            Page = self.Page,
            Section = self,
        }

        local Items = { } do
            Items["Divider"] = Instances:Create("Frame", {
                Parent = Divider.Section.Elements["Content"].Instance,
                BackgroundTransparency = 1,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 10),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 

            Items["RealDivider"] = Instances:Create("Frame", {
                Parent = Items["Divider"].Instance,
                AnchorPoint = Vector2New(0, 0.5),
                Name = "\0",
                Position = UDim2New(0, 0, 0.5, 0),
                BorderColor3 = FromRGB(10, 10, 10),
                Size = UDim2New(1, 0, 0, 3),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(15, 15, 20)
            })  Items["RealDivider"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})

            Instances:Create("UIStroke", {
                Parent = Items["RealDivider"].Instance,
                Color = FromRGB(27, 27, 32),
                Name = "\0",
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border
            }):AddToTheme({Color = "Outline"})
        end
        
        function Divider:SetVisibility(Bool)
            Items["Divider"].Instance.Visible = Bool
        end

        return Divider
    end

    Library.Sections.Toggle = function(self, Data)
        Data = Data or { }

        local Toggle = {
            Window = self.Window,
            Page = self.Page,
            Section = self,

            Name = Data.Name or Data.name or "Toggle",
            Flag = Data.Flag or Data.flag or Library:NextFlag(),
            Default = Data.Default or Data.default or false,
            Callback = Data.Callback or Data.callback or function() end,

            Value = false,
            Class = "Toggle",

            Count = 0
        }

        local Items = { } do 
            Items["Toggle"] = Instances:Create("TextButton", {
                Parent = Toggle.Section.Elements["Content"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "",
                AutoButtonColor = false,
                BackgroundTransparency = 1,
                Name = "\0",
                Size = UDim2New(1, 0, 0, 11),
                BorderSizePixel = 0,
                TextSize = 14,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["Indicator"] = Instances:Create("Frame", {
                Parent = Items["Toggle"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(10, 10, 10),
                Size = UDim2New(0, 10, 0, 10),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(33, 33, 36)
            })  Items["Indicator"]:AddToTheme({BackgroundColor3 = "Element", BorderColor3 = "Border"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Indicator"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Instances:Create("UIGradient", {
                Parent = Items["Indicator"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(100, 100, 100))}
            }) 
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Toggle"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                TextTransparency = 0.48,
                Text = Toggle.Name,
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                Position = UDim2New(0, 18, 0, -1),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                BorderSizePixel = 0,
                BorderColor3 = FromRGB(0, 0, 0),
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})

            Items["Toggle"]:OnHover(function()
                if Toggle.Value then 
                    return 
                end

                Items["Indicator"]:Tween(nil, {BackgroundColor3 = Library.Theme["Hovered Element"]})
                Items["Indicator"]:ChangeItemTheme({BackgroundColor3 = "Hovered Element", BorderColor3 = "Border"})
            end)

            Items["Toggle"]:OnHoverLeave(function()
                if Toggle.Value then 
                    return 
                end

                Items["Indicator"]:Tween(nil, {BackgroundColor3 = Library.Theme["Element"]})
                Items["Indicator"]:ChangeItemTheme({BackgroundColor3 = "Element", BorderColor3 = "Border"})
            end)
        end
        
        function Toggle:Get()
            return Toggle.Value
        end

        function Toggle:Set(Bool)
            Toggle.Value = Bool or not Toggle.Value

            Library.Flags[Toggle.Flag] = Toggle.Value

            if Toggle.Value then 
                Items["Indicator"]:ChangeItemTheme({BackgroundColor3 = "Accent"})

                Items["Indicator"]:Tween(nil, {BackgroundColor3 = Library.Theme.Accent})
                Items["Text"]:Tween(nil, {TextTransparency = 0})
            else
                Items["Indicator"]:ChangeItemTheme({BackgroundColor3 = "Element"})

                Items["Indicator"]:Tween(nil, {BackgroundColor3 = Library.Theme.Element})
                Items["Text"]:Tween(nil, {TextTransparency = 0.48})
            end

            if Toggle.Callback then 
                Library:SafeCall(Toggle.Callback, Toggle.Value)
            end
        end

        function Toggle:SetVisiblity(Bool)
            Items["Toggle"].Instance.Visible = Bool
        end

        function Toggle:Colorpicker(Data)
            Data = Data or { }

            local Colorpicker = {
                Window = self.Window,
                Tab = self.Tab,
                Section = self.Section,

                Parent = Items["Toggle"],
                Name = Data.Name or Data.name or "Colorpicker",
                Flag = Data.Flag or Data.flag or Library:NextFlag(),
                Default = Data.Default or Data.default or Color3.fromRGB(255, 255, 255),
                Callback = Data.Callback or Data.callback or function() end,
                Alpha = Data.Alpha or Data.alpha or false,
                Count = Toggle.Count,

                FadeSpeed = self.Window.FadeSpeed
            }

            Toggle.Count += 1
            Colorpicker.Count = Toggle.Count

            local Extension = Library:CreateColorpicker(Colorpicker)
            Library.Flags[Colorpicker.Flag] = Extension

            return Colorpicker
        end

        function Toggle:Keybind(Data)
            Data = Data or { }

            local Keybind = {
                Window = self.Window,
                Tab = self.Tab,
                Section = self.Section,

                Parent = Items["Toggle"],
                Name = Data.Name or Data.name or "Keybind",
                Flag = Data.Flag or Data.flag or Library:NextFlag(),
                Default = Data.Default or Data.default or "MB2",
                Mode = Data.Mode or Data.mode or "Toggle",
                Callback = Data.Callback or Data.callback or function() end,
            }

            local Extension = Library:CreateKeybind(Keybind)
            Library.Flags[Keybind.Flag] = Extension

            return Keybind, Extension
        end

        Items["Toggle"]:Connect("MouseButton1Down", function()
            Toggle:Set()
        end)

        if Toggle.Default then 
            Toggle:Set(Toggle.Default)
        end

        Library.SetFlags[Toggle.Flag] = function(Value)
            Toggle:Set(Value)
        end

        return Toggle
    end

    Library.Sections.Button = function(self, Data)
        Data = Data or { }

        local Button = {
            Window = self.Window,
            Page = self.Page,
            Section = self,

            Name = Data.Name or Data.name,
            Callback = Data.Callback or Data.callback or function() end,
        }

        local Items = { } do 
            Items["Button"] = Instances:Create("TextButton", {
                Parent = Button.Section.Elements["Content"].Instance,
                BorderColor3 = FromRGB(10, 10, 10),
                AutoButtonColor = false,
                Name = "\0",
                Position = UDim2New(0, 0, 1, 0),
                Size = UDim2New(1, 0, 0, 17),
                Selectable = false,
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(33, 33, 36)
            })  Items["Button"]:AddToTheme({BackgroundColor3 = "Element", BorderColor3 = "Border"})

            Instances:Create("UIGradient", {
                Parent = Items["Button"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(100, 100, 100))}
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["Button"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"}) 
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Button"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Button.Name,
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BackgroundTransparency = 1,
                TextTruncate = Enum.TextTruncate.AtEnd,
                Position = UDim2New(0, 0, 0, -1),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Items["TextBorder"] = Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})

            Items["Button"]:OnHover(function()
                Items["Button"]:Tween(nil, {BackgroundColor3 = Library.Theme["Hovered Element"]})
                Items["Button"]:ChangeItemTheme({BackgroundColor3 = "Hovered Element", BorderColor3 = "Border"})
            end)

            Items["Button"]:OnHoverLeave(function()
                Items["Button"]:Tween(nil, {BackgroundColor3 = Library.Theme["Element"]})
                Items["Button"]:ChangeItemTheme({BackgroundColor3 = "Element", BorderColor3 = "Border"})
            end)
        end

        function Button:Press()
            Library:SafeCall(Button.Callback)

            Items["Text"]:ChangeItemTheme({TextColor3 = "Accent"})
            Items["Button"]:ChangeItemTheme({BackgroundColor3 = "Accent"})

            Items["Text"]:Tween(nil, {TextColor3 = Library.Theme.Accent})
            Items["Button"]:Tween(nil, {BackgroundColor3 = Library.Theme.Accent})

            task.wait(0.1)

            Items["Text"]:ChangeItemTheme({TextColor3 = "Text"})
            Items["Button"]:ChangeItemTheme({BackgroundColor3 = "Element"})

            Items["Text"]:Tween(nil, {TextColor3 = Library.Theme.Text})
            Items["Button"]:Tween(nil, {BackgroundColor3 = Library.Theme.Element})
        end

        function Button:SetVisiblity(Bool)
            Items["Button"].Instance.Visible = Bool
        end

        Items["Button"]:Connect("MouseButton1Down", function()
            Button:Press()
        end)

        return Button
    end

    Library.Sections.Slider = function(self, Data)
        Data = Data or { }

        local Slider = {
            Window = self.Window,
            Page = self.Page,
            Section = self,

            Name = Data.Name or Data.name or "Slider",
            Flag = Data.Flag or Data.flag or Library:NextFlag(),
            Min = Data.Min or Data.min or 0,
            Default = Data.Default or Data.default or 0,
            Max = Data.Max or Data.max or 100,
            Suffix = Data.Suffix or Data.suffix or "",
            Decimals = Data.Decimals or Data.decimals or 1,
            Callback = Data.Callback or Data.callback or function() end,
            Compact = Data.Compact or Data.compact or false,

            Value = 0,
            Sliding = false,
            Class = "Slider",
        }

        local Items = { } do 
            Items["Slider"] = Instances:Create("Frame", {
                Parent = Slider.Section.Elements["Content"].Instance,
                BackgroundTransparency = 1,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 27),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Slider"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Slider.Name,
                Name = "\0",
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Size = UDim2New(1, 0, 0, 13),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["RealSlider"] = Instances:Create("TextButton", {
                Parent = Items["Slider"].Instance,
                AnchorPoint = Vector2New(0, 1),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 0),
                BorderColor3 = FromRGB(10, 10, 10),
                Text = "",
                AutoButtonColor = false,
                Size = UDim2New(1, 0, 0, 10),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(33, 33, 36)
            })  Items["RealSlider"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})
            
            Instances:Create("UIStroke", {
                Parent = Items["RealSlider"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Instances:Create("UIGradient", {
                Parent = Items["RealSlider"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(100, 100, 100))}
            }) 
            
            Items["Indicator"] = Instances:Create("Frame", {
                Parent = Items["RealSlider"].Instance,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(0.5, 0, 1, 0),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(235, 157, 255)
            })  Items["Indicator"]:AddToTheme({BackgroundColor3 = "Accent"})
            
            Instances:Create("UIGradient", {
                Parent = Items["Indicator"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(100, 100, 100))}
            }) 
            
            Items["Value"] = Instances:Create("TextLabel", {
                Parent = Items["RealSlider"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "50/100s",
                Name = "\0",
                BackgroundTransparency = 1,
                Position = UDim2New(0, 0, 0, -1),
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Value"]:AddToTheme({TextColor3 = "Text"})

            Instances:Create("UIStroke", {
                Parent = Items["Value"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})

            if Slider.Compact then 
                Items["Value"]:Clean()
                Items["Value"] = nil

                Items["Slider"].Instance.Size = UDim2New(1,0,0,10)
                Items["Text"].Instance.Parent = Items["RealSlider"].Instance
                Items["Text"].Instance.Position = UDim2New(0,0,0,-2)
                Items["Text"].Instance.TextXAlignment = Enum.TextXAlignment.Center
            end

            Items["RealSlider"]:OnHover(function()
                Items["RealSlider"]:Tween(nil, {BackgroundColor3 = Library.Theme["Hovered Element"]})
                Items["RealSlider"]:ChangeItemTheme({BackgroundColor3 = "Hovered Element", BorderColor3 = "Border"})
            end)

            Items["RealSlider"]:OnHoverLeave(function()
                Items["RealSlider"]:Tween(nil, {BackgroundColor3 = Library.Theme["Background"]})
                Items["RealSlider"]:ChangeItemTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})
            end)
        end

        function Slider:Set(Value)
            Slider.Value = MathClamp(Library:Round(Value, Slider.Decimals), Slider.Min, Slider.Max)

            Library.Flags[Slider.Flag] = Slider.Value
            
            if Slider.Compact then
                Items["Text"].Instance.Text = `{Slider.Name}: {Slider.Value}{Slider.Suffix}`
            else
                Items["Value"].Instance.Text = `{Slider.Value}{Slider.Suffix}`
            end

            Items["Indicator"]:Tween(TweenInfo.new(0.17, Enum.EasingStyle.Quart, Enum.EasingDirection.Out), {Size = UDim2New((Slider.Value - Slider.Min) / (Slider.Max - Slider.Min), 0, 1, 0)})

            if Slider.Callback then 
                Library:SafeCall(Slider.Callback, Slider.Value)
            end
        end

        function Slider:Get()
            return Slider.Value
        end

        function Slider:SetVisibility(Bool)
            Items["Slider"].Instance.Visible = Bool
        end

        Items["RealSlider"]:Connect("MouseButton1Down", function()
            Slider.Sliding = true

            local MousePos = UserInputService:GetMouseLocation()

            local SizeX = (MousePos.X - Items["RealSlider"].Instance.AbsolutePosition.X) / Items["RealSlider"].Instance.AbsoluteSize.X
            local Value = ((Slider.Max - Slider.Min) * SizeX) + Slider.Min

            Slider:Set(Value)
        end)

        Items["RealSlider"]:Connect("InputEnded", function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseButton1 then
                Slider.Sliding = false
            end
        end)

        Library:Connect(UserInputService.InputChanged, function(Input)
            if Input.UserInputType == Enum.UserInputType.MouseMovement and Slider.Sliding then
                local MousePos = UserInputService:GetMouseLocation()

                local SizeX = (MousePos.X - Items["RealSlider"].Instance.AbsolutePosition.X) / Items["RealSlider"].Instance.AbsoluteSize.X
                local Value = ((Slider.Max - Slider.Min) * SizeX) + Slider.Min

                Slider:Set(Value)
            end
        end)

        if Slider.Default then
            Slider:Set(Slider.Default)
        end

        Library.SetFlags[Slider.Flag] = function(Value)
            Slider:Set(Value)
        end

        return Slider
    end

    Library.Sections.Dropdown = function(self, Data)
        Data = Data or { }

        local Dropdown = {
            Window = self.Window,
            Page = self.Page,
            Section = self,

            Name = Data.Name or Data.name or "Dropdown",
            Flag = Data.Flag or Data.flag or Library:NextFlag(),
            Items = Data.Items or Data.items or { "One", "Two", "Three" },
            Default = Data.Default or Data.default or nil,
            Callback = Data.Callback or Data.callback or function() end,
            Multi = Data.Multi or Data.multi or false,

            Value = { },
            IsOpen = false,
            Options = { },
            Class = "Dropdown",
        }

        local Items = { } do
            Items["Dropdown"] = Instances:Create("Frame", {
                Parent = Dropdown.Section.Elements["Content"].Instance,
                BackgroundTransparency = 1,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 34),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Dropdown"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Dropdown.Name,
                Name = "\0",
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Size = UDim2New(1, 0, 0, 13),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})

            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["RealDropdown"] = Instances:Create("Frame", {
                Parent = Items["Dropdown"].Instance,
                AnchorPoint = Vector2New(0, 1),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 0),
                BorderColor3 = FromRGB(10, 10, 10),
                Size = UDim2New(1, 0, 0, 17),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(33, 33, 36)
            })  Items["RealDropdown"]:AddToTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})
            
            Instances:Create("UIGradient", {
                Parent = Items["RealDropdown"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(100, 100, 100))}
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["RealDropdown"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["Open"] = Instances:Create("TextButton", {
                Parent = Items["RealDropdown"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "+",
                AutoButtonColor = false,
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Right,
                Position = UDim2New(0, -4, 0, -1),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Open"]:AddToTheme({TextColor3 = "Text"})

            Instances:Create("UIStroke", {
                Parent = Items["Open"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"}) 
            
            Items["Value"] = Instances:Create("TextLabel", {
                Parent = Items["RealDropdown"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "--",
                Name = "\0",
                Size = UDim2New(1, -25, 1, 0),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                TextTruncate = Enum.TextTruncate.AtEnd,
                Position = UDim2New(0, 5, 0, -1),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Value"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Value"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["OptionHolder"] = Instances:Create("Frame", {
                Parent = Items["Dropdown"].Instance,
                Visible = false,
                BorderColor3 = FromRGB(10, 10, 10),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 5),
                Size = UDim2New(1, 0, 0, 0),
                BorderSizePixel = 2,
                AutomaticSize = Enum.AutomaticSize.Y,
                BackgroundColor3 = FromRGB(20, 20, 25)
            })  Items["OptionHolder"]:AddToTheme({BackgroundColor3 = "Inline", BorderColor3 = "Border"})
            
            Instances:Create("UIStroke", {
                Parent = Items["OptionHolder"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})

            Instances:Create("UIListLayout", {
                Parent = Items["OptionHolder"].Instance,
                SortOrder = Enum.SortOrder.LayoutOrder
            }) 
            
            Instances:Create("UIPadding", {
                Parent = Items["OptionHolder"].Instance,
                PaddingBottom = UDimNew(0, 2)
            })

            Items["RealDropdown"]:OnHover(function()
                Items["RealDropdown"]:Tween(nil, {BackgroundColor3 = Library.Theme["Hovered Element"]})
                Items["RealDropdown"]:ChangeItemTheme({BackgroundColor3 = "Hovered Element", BorderColor3 = "Border"})
            end)

            Items["RealDropdown"]:OnHoverLeave(function()
                Items["RealDropdown"]:Tween(nil, {BackgroundColor3 = Library.Theme["Background"]})
                Items["RealDropdown"]:ChangeItemTheme({BackgroundColor3 = "Background", BorderColor3 = "Border"})
            end)
        end

        function Dropdown:Set(Option)
            if Dropdown.Multi then 
                if type(Option) ~= "table" then 
                    return
                end

                Dropdown.Value = Option

                for Index, Value in Option do 
                    local OptionData = Dropdown.Options[Value]
                    
                    if not OptionData then 
                        return
                    end

                    OptionData.Selected = true
                    OptionData:Toggle("Active")
                end

                Library.Flags[Dropdown.Flag] = Dropdown.Value

                Items["Value"].Instance.Text = TableConcat(Option, ", ")
            else
                if not Dropdown.Options[Option] then 
                    return
                end

                local OptionData = Dropdown.Options[Option]

                Dropdown.Value = OptionData.Name

                OptionData.Selected = true
                OptionData:Toggle("Active")

                for Index, Value in Dropdown.Options do 
                    if Value ~= OptionData then 
                        Value.Selected = false
                        Value:Toggle("Inactive")
                    end
                end

                Library.Flags[Dropdown.Flag] = Dropdown.Value

                Items["Value"].Instance.Text = Option
            end

            if Dropdown.Callback then 
                Library:SafeCall(Dropdown.Callback, Option)
            end
        end

        function Dropdown:Get()
            return Dropdown.Value
        end

        function Dropdown:SetVisibility(Bool)
            Items["Dropdown"].Instance.Visible = Bool
        end

        function Dropdown:Add(Option)
            local OptionButton = Instances:Create("TextButton", {
                Parent = Items["OptionHolder"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "",
                AutoButtonColor = false,
                Name = "\0",
                BackgroundTransparency = 1,
                BorderSizePixel = 0,
                Size = UDim2New(1, 0, 0, 15),
                ZIndex = 5,
                TextSize = 14,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            local OptionText = Instances:Create("TextLabel", {
                Parent = OptionButton.Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                TextTransparency = 0.48,
                Text = Option,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, -5, 1, 0),
                Position = UDim2New(0, 5, 0, 0),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                BorderSizePixel = 0,
                ZIndex = 5,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            OptionText:AddToTheme({TextColor3 = "Text"})

            Instances:Create("UIStroke", {
                Parent = OptionText.Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})

            local OptionData = {
                Selected = false,
                Name = Option,
                Text = OptionText,
                Button = OptionButton
            }

            function OptionData:Toggle(State)
                if State == "Active" then 
                    OptionData.Text:ChangeItemTheme({TextColor3 = "Accent"})
                    OptionData.Text:Tween(nil, {TextColor3 = Library.Theme.Accent, TextTransparency = 0})
                else
                    OptionData.Text:ChangeItemTheme({TextColor3 = "Text"})
                    OptionData.Text:Tween(nil, {TextColor3 = Library.Theme.Text, TextTransparency = 0.48})
                end
            end

            function OptionData:Set()
                OptionData.Selected = not OptionData.Selected

                if Dropdown.Multi then
                    local Index = TableFind(Dropdown.Value, OptionData.Name)

                    if Index then 
                        TableRemove(Dropdown.Value, Index)
                    else
                        TableInsert(Dropdown.Value, OptionData.Name)
                    end

                    Library.Flags[Dropdown.Flag] = Dropdown.Value

                    OptionData:Toggle(Index and "Inactive" or "Active")

                    local TextFormat = #Dropdown.Value > 0 and TableConcat(Dropdown.Value, ", ") or "--"

                    Items["Value"].Instance.Text = TextFormat
                else
                    if OptionData.Selected then
                        Dropdown.Value = OptionData.Name

                        Library.Flags[Dropdown.Flag] = Dropdown.Value

                        OptionData:Toggle("Active")
                        Items["Value"].Instance.Text = OptionData.Name

                        for Index, Value in Dropdown.Options do 
                            if Value ~= OptionData then 
                                Value.Selected = false
                                Value:Toggle("Inactive")
                            end
                        end
                    else
                        Dropdown.Value = nil

                        OptionData:Toggle("Inactive")
                        Items["Value"].Instance.Text = "--"
                    end
                end

                if Dropdown.Callback then 
                    Library:SafeCall(Dropdown.Callback, Dropdown.Value)
                end
            end

            OptionButton:Connect("MouseButton1Down", function()
                OptionData:Set()
            end)

            Dropdown.Options[Option] = OptionData
            return OptionData
        end

        function Dropdown:Remove(Option)
            if Dropdown.Options[Option] then 
                Dropdown.Options[Option].Button:Clean()
            end
        end

        function Dropdown:Refresh(List)
            for Index, Value in Dropdown.Options do 
                Dropdown:Remove(Value.Name)
            end

            for Index, Value in List do 
                Dropdown:Add(Value)
            end
        end

        local Debounce = false

        function Dropdown:SetOpen(Bool)
            if Debounce then 
                return 
            end

            Dropdown.IsOpen = Bool

            Debounce = true 

            if Bool then 
                Items["OptionHolder"].Instance.Visible = true
                Items["OptionHolder"].Instance.ZIndex = 15
                Items["Open"].Instance.Text = "-"
                Items["Open"].Instance.Position = UDim2New(0, -5, 0, -1)
            else
                Items["Open"].Instance.Text = "+"
                Items["Open"].Instance.Position = UDim2New(0, -4, 0, -1)
            end

            local Descendants = Items["OptionHolder"].Instance:GetDescendants()
            TableInsert(Descendants, Items["OptionHolder"].Instance)

            local NewTween
            for Index, Value in Descendants do 
                local ValueIndex = Library:GetTransparencyPropertyFromItem(Value)

                if not ValueIndex then 
                    continue
                end

                if not StringFind(Value.ClassName, "UI") then 
                    Value.ZIndex = Bool and 15 or 1
                end

                if type(ValueIndex) == "table" then
                    for _, Property in ValueIndex do 
                        NewTween = Library:FadeItem(Value, Property, Bool, Dropdown.Window.FadeSpeed)
                    end
                else
                    NewTween = Library:FadeItem(Value, ValueIndex, Bool, Dropdown.Window.FadeSpeed)
                end
            end

            Library:Connect(NewTween.Tween.Completed, function()
                Debounce = false
                Items["OptionHolder"].Instance.Visible = Bool
                Items["OptionHolder"].Instance.ZIndex = Bool and 15 or 1
            end)
        end

        for Index, Value in Dropdown.Items do 
            Dropdown:Add(Value)
        end

        Items["Open"]:Connect("MouseButton1Down", function()
            Dropdown:SetOpen(not Dropdown.IsOpen)
        end)

        if Dropdown.Default then 
            Dropdown:Set(Dropdown.Default)
        end

        Library.SetFlags[Dropdown.Flag] = function(Value)
            Dropdown:Set(Value)            
        end

        return Dropdown
    end

    Library.Sections.Label = function(self, Data)
        Data = Data or { }

        local Label = {
            Window = self.Window,
            Page = self.Page,
            Section = self,

            Name = Data.Name or Data.name,
            Alignment = Data.Alignment or Data.alignment or "Left",

            Count = 0
        }

        local Items = { } do 
            Items["Label"] = Instances:Create("Frame", {
                Parent = Label.Section.Elements["Content"].Instance,
                BackgroundTransparency = 1,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 15),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Label"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Label.Name,
                Name = "\0",
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment[Label.Alignment],
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})

            Instances:Create("UIStroke", {
                ApplyStrokeMode = Enum.ApplyStrokeMode.Contextual,
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
            }):AddToTheme({Color = "Text Border"})
        end

        function Label:Colorpicker(Data)
            Data = Data or { }

            local Colorpicker = {
                Window = self.Window,
                Tab = self.Tab,
                Section = self.Section,

                Parent = Items["Label"],
                Name = Data.Name or Data.name or "Colorpicker",
                Flag = Data.Flag or Data.flag or Library:NextFlag(),
                Default = Data.Default or Data.default or Color3.fromRGB(255, 255, 255),
                Callback = Data.Callback or Data.callback or function() end,
                Alpha = Data.Alpha or Data.alpha or false,
                Count = Label.Count,
                FadeSpeed = self.Window.FadeSpeed
            }

            Label.Count += 1
            Colorpicker.Count = Label.Count

            local Extension = Library:CreateColorpicker(Colorpicker)
            
            return Colorpicker, Extension
        end

        function Label:Keybind(Data)
            Data = Data or { }

            local Keybind = {
                Window = self.Window,
                Tab = self.Tab,
                Section = self.Section,

                Parent = Items["Label"],
                Name = Data.Name or Data.name or "Keybind",
                Flag = Data.Flag or Data.flag or Library:NextFlag(),
                Default = Data.Default or Data.default or "MB2",
                Mode = Data.Mode or Data.mode or "Toggle",
                Callback = Data.Callback or Data.callback or function() end,
            }

            local Extension = Library:CreateKeybind(Keybind)

            return Keybind, Extension
        end

        return Label
    end

    Library.Sections.Textbox = function(self, Data)
        Data = Data or { }

        local Textbox = {
            Window = self.Window,
            Tab = self.Tab,
            Section = self,

            Name = Data.Name or Data.name or "Textbox",
            Flag = Data.Flag or Data.flag or Library:NextFlag(),
            Placeholder = Data.Placeholder or Data.placeholder or "...",
            Default = Data.Default or Data.default or "",
            Callback = Data.Callback or Data.callback or function() end,

            Value = "",
            Class = "Textbox"
        }

        local Items = { } do 
            Items["Textbox"] = Instances:Create("Frame", {
                Parent = Textbox.Section.Elements["Content"].Instance,
                BackgroundTransparency = 1,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, 0, 0, 34),
                BorderSizePixel = 0,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["Text"] = Instances:Create("TextLabel", {
                Parent = Items["Textbox"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = Textbox.Name,
                Name = "\0",
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Left,
                Size = UDim2New(1, 0, 0, 13),
                BorderSizePixel = 0,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Text"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIStroke", {
                Parent = Items["Text"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})
            
            Items["Background"] = Instances:Create("Frame", {
                Parent = Items["Textbox"].Instance,
                AnchorPoint = Vector2New(0, 1),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 0),
                BorderColor3 = FromRGB(10, 10, 10),
                Size = UDim2New(1, 0, 0, 17),
                BorderSizePixel = 2,
                BackgroundColor3 = FromRGB(33, 33, 36)
            })  Items["Background"]:AddToTheme({BackgroundColor3 = "Element", BorderColor3 = "Border"})
            
            Instances:Create("UIGradient", {
                Parent = Items["Background"].Instance,
                Rotation = 90,
                Color = RGBSequence{RGBSequenceKeypoint(0, FromRGB(255, 255, 255)), RGBSequenceKeypoint(1, FromRGB(100, 100, 100))}
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["Background"].Instance,
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0",
                Color = FromRGB(27, 27, 32)
            }):AddToTheme({Color = "Outline"})
            
            Items["Inline"] = Instances:Create("TextBox", {
                Parent = Items["Background"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "",
                Name = "\0",
                Size = UDim2New(1, 0, 1, 0),
                BorderSizePixel = 0,
                ClearTextOnFocus = false,
                BackgroundTransparency = 1,
                PlaceholderColor3 = FromRGB(178, 178, 178),
                TextXAlignment = Enum.TextXAlignment.Left,
                PlaceholderText = Textbox.Placeholder,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            })  Items["Inline"]:AddToTheme({TextColor3 = "Text"})
            
            Instances:Create("UIPadding", {
                Parent = Items["Inline"].Instance,
                PaddingBottom = UDimNew(0, 3),
                PaddingLeft = UDimNew(0, 5)
            }) 
            
            Instances:Create("UIStroke", {
                Parent = Items["Inline"].Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})

            Items["Background"]:OnHover(function()
                Items["Background"]:Tween(nil, {BackgroundColor3 = Library.Theme["Hovered Element"]})
                Items["Background"]:ChangeItemTheme({BackgroundColor3 = "Hovered Element", BorderColor3 = "Border"})
            end)

            Items["Background"]:OnHoverLeave(function()
                Items["Background"]:Tween(nil, {BackgroundColor3 = Library.Theme["Element"]})
                Items["Background"]:ChangeItemTheme({BackgroundColor3 = "Element", BorderColor3 = "Border"})
            end)
        end

        function Textbox:Get()
            return Textbox.Value
        end

        function Textbox:SetVisibility(Bool)
            Items["Textbox"].Instance.Visible = Bool
        end

        function Textbox:Set(Value)
            Textbox.Value = Value
            
            Items["Inline"].Instance.Text = Textbox.Value
            Items["Inline"]:Tween(nil, {TextColor3 = Library.Theme.Text})
            Items["Inline"]:ChangeItemTheme({TextColor3 = "Text"})

            Library.Flags[Textbox.Flag] = Textbox.Value

            if Textbox.Callback then
                Library:SafeCall(Textbox.Callback, Textbox.Value)
            end
        end

        Items["Inline"]:Connect("Focused", function()
            Items["Inline"]:ChangeItemTheme({TextColor3 = "Accent"})
            Items["Inline"]:Tween(nil, {TextColor3 = Library.Theme.Accent})
        end)

        Items["Inline"]:Connect("FocusLost", function()
            Items["Inline"]:ChangeItemTheme({TextColor3 = "Text"})
            Items["Inline"]:Tween(nil, {TextColor3 = Library.Theme.Text})

            Textbox:Set(Items["Inline"].Instance.Text)
        end)

        if Textbox.Default then
            Textbox:Set(Textbox.Default)
        end

        Library.SetFlags[Textbox.Flag] = function(Value)
            Textbox:Set(Value)
        end

        return Textbox
    end
    
    Library.Sections.Listbox = function(self, Data)
        Data = Data or {}

        local Listbox = {
            Window = self.Window,
            Page = self.Page,
            Section = self,

            Items = Data.Items or Data.items or { },
            Multi = Data.Multi or Data.multi or false,
            Default = Data.Default or Data.default or 1,
            Flag = Data.Flag or Data.flag or Library:NextFlag(),
            Callback = Data.Callback or Data.callback or function() end,
            Size = Data.Size or Data.size or 175,

            Value = { },
            Options = { },
            Class = "Listbox",
        }

        local Items = { } do 
            Items["Listbox"] = Instances:Create("Frame", {
                Parent = Listbox.Section.Elements["Content"].Instance,
                Name = "\0",
                BackgroundTransparency = 1,
                Size = UDim2New(1, 0, 0, Listbox.Size),
                BorderColor3 = FromRGB(0, 0, 0),
                BorderSizePixel = 0,
                AutomaticSize = Enum.AutomaticSize.Y,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            Items["RealListbox"] = Instances:Create("ScrollingFrame", {
                Parent = Items["Listbox"].Instance,
                ScrollBarImageColor3 = FromRGB(235, 157, 255),
                Active = true,
                AutomaticCanvasSize = Enum.AutomaticSize.Y,
                ScrollBarThickness = 1,
                AnchorPoint = Vector2New(0, 1),
                Size = UDim2New(1, 0, 1, 0),
                Name = "\0",
                Position = UDim2New(0, 0, 1, 0),
                BackgroundColor3 = FromRGB(15, 15, 20),
                BorderColor3 = FromRGB(10, 10, 10),
                BorderSizePixel = 2,
                CanvasSize = UDim2New(0, 0, 0, 0)
            })  Items["RealListbox"]:AddToTheme({ScrollBarImageColor3 = "Accent", BackgroundColor3 = "Background", BorderColor3 = "Border"})
            
            Instances:Create("UIStroke", {
                Parent = Items["RealListbox"].Instance,
                Color = FromRGB(27, 27, 32),
                Name = "\0",
                ApplyStrokeMode = Enum.ApplyStrokeMode.Border
            }):AddToTheme({Color = "Outline"}) 
            
            Instances:Create("UIListLayout", {
                Parent = Items["RealListbox"].Instance,
                SortOrder = Enum.SortOrder.LayoutOrder
            }) 

            Instances:Create("UIPadding", {
                Parent = Items["RealListbox"].Instance,
                PaddingBottom = UDimNew(0, 5),
                PaddingTop = UDimNew(0, 2)
            }) 
        end

        function Listbox:Set(Option)
            if Listbox.Multi then 
                if type(Option) ~= "table" then 
                    return
                end

                Listbox.Value = Option

                Library.Flags[Listbox.Flag] = Listbox.Value

                for Index, Value in Option do 
                    local OptionData = Listbox.Options[Value]
                    
                    if not OptionData then 
                        return
                    end

                    OptionData.Selected = true
                    OptionData:Toggle("Active")
                end
            else
                if not Listbox.Options[Option] then 
                    return
                end

                local OptionData = Listbox.Options[Option]

                Listbox.Value = OptionData.Name
                
                Library.Flags[Listbox.Flag] = Listbox.Value

                OptionData.Selected = true
                OptionData:Toggle("Active")

                for Index, Value in Listbox.Options do 
                    if Value ~= OptionData then 
                        Value.Selected = false
                        Value:Toggle("Inactive")
                    end
                end
            end

            if Listbox.Callback then 
                Library:SafeCall(Listbox.Callback, Option)
            end
        end

        function Listbox:Get()
            return Listbox.Value
        end

        function Listbox:SetVisibility(Bool)
            Items["Listbox"].Instance.Visible = Bool
        end

        function Listbox:Remove(Option)
            if Listbox.Options[Option] then 
                Listbox.Options[Option].Button:Clean()
            end
        end

        function Listbox:Refresh(List)
            for Index, Value in Listbox.Options do 
                Listbox:Remove(Value.Name)
            end

            for Index, Value in List do 
                Listbox:Add(Value)
            end
        end

        function Listbox:Add(Option)
            local OptionButton = Instances:Create("TextButton", {
                Parent = Items["RealListbox"].Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(0, 0, 0),
                BorderColor3 = FromRGB(0, 0, 0),
                Text = "",
                AutoButtonColor = false,
                Name = "\0",
                BackgroundTransparency = 1,
                BorderSizePixel = 0,
                Size = UDim2New(1, 0, 0, 15),
                ZIndex = 5,
                TextSize = 14,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            local OptionText = Instances:Create("TextLabel", {
                Parent = OptionButton.Instance,
                FontFace = Library.Font,
                TextColor3 = FromRGB(215, 215, 215),
                TextTransparency = 0.48,
                Text = Option,
                Name = "\0",
                BorderColor3 = FromRGB(0, 0, 0),
                Size = UDim2New(1, -5, 1, 0),
                Position = UDim2New(0, 5, 0, 0),
                BackgroundTransparency = 1,
                TextXAlignment = Enum.TextXAlignment.Center,
                BorderSizePixel = 0,
                ZIndex = 5,
                TextSize = 12,
                BackgroundColor3 = FromRGB(255, 255, 255)
            }) 
            
            OptionText:AddToTheme({TextColor3 = "Text"})

            Instances:Create("UIStroke", {
                Parent = OptionText.Instance,
                LineJoinMode = Enum.LineJoinMode.Miter,
                Name = "\0"
            }):AddToTheme({Color = "Text Border"})

            local OptionData = {
                Selected = false,
                Name = Option,
                Text = OptionText,
                Button = OptionButton
            }

            function OptionData:Toggle(State)
                if State == "Active" then 
                    OptionData.Text:ChangeItemTheme({TextColor3 = "Accent"})
                    OptionData.Text:Tween(nil, {TextColor3 = Library.Theme.Accent, TextTransparency = 0})
                else
                    OptionData.Text:ChangeItemTheme({TextColor3 = "Text"})
                    OptionData.Text:Tween(nil, {TextColor3 = Library.Theme.Text, TextTransparency = 0.48})
                end
            end

            function OptionData:Set()
                OptionData.Selected = not OptionData.Selected

                if Listbox.Multi then
                    local Index = TableFind(Listbox.Value, OptionData.Name)

                    if Index then 
                        TableRemove(Listbox.Value, Index)
                    else
                        TableInsert(Listbox.Value, OptionData.Name)
                    end

                    OptionData:Toggle(Index and "Inactive" or "Active")

                    local TextFormat = #Listbox.Value > 0 and TableConcat(Listbox.Value, ", ") or "--"
                else
                    if OptionData.Selected then
                        Listbox.Value = OptionData.Name

                        OptionData:Toggle("Active")

                        for Index, Value in Listbox.Options do 
                            if Value ~= OptionData then 
                                Value.Selected = false
                                Value:Toggle("Inactive")
                            end
                        end
                    else
                        Listbox.Value = nil

                        OptionData:Toggle("Inactive")
                    end
                end

                if Listbox.Callback then 
                    Library:SafeCall(Listbox.Callback, Listbox.Value)
                end
            end

            OptionButton:Connect("MouseButton1Down", function()
                OptionData:Set()
            end)

            Listbox.Options[Option] = OptionData
            return OptionData
        end

        for Index, Value in Listbox.Items do 
            Listbox:Add(Value)
        end

        if Listbox.Default then 
            Listbox:Set(Listbox.Default)
        end

        Library.SetFlags[Listbox.Flag] = function(Value)
            Listbox:Set(Value)
        end

        return Listbox
    end
end

getgenv().Library = Library

---------------------------------------[[ Extra ]]--------------------------------------- 
DownloadImage = function(Link, Path, Name)
    local Data = request({Url = Link}).Body
    writefile(Path..Name..".png", Data)
end

DownloadImage("https://i.imgur.com/vd0r7AH.jpeg", "matcha/", "Super Cute Cat")
DownloadImage("https://i.imgur.com/vd0r7AH.jpeg", "matcha/Images/", "Reallyyyy Cute Cat")
DownloadImage("https://i.imgur.com/vd0r7AH.jpeg", "", "SUPER DUPER CUTE CAT")

---------------------------------------[[ Start ]]---------------------------------------

-- Prestart
if not LPH_OBFUSCATED then
	LPH_NO_VIRTUALIZE = function(f, ...)
		assert(type(f) == "function" and #{...} == 0, "LPH_NO_VIRTUALIZE only accepts a single constant function as an argument.")
		return f
	end
end		
if not isfolder("matcha/Assets") then
    makefolder("matcha/Assets")
end
if not isfolder("matcha/Characters") then
    makefolder("matcha/Characters")
end
if not isfile("matcha/Characters/Base.Character") then
    writefile("matcha/Characters/Base.Character", [[
local CharacterSettings = {}

CharacterSettings.Shirt = 18596812870
CharacterSettings.Pants = 14287253187
CharacterSettings.Head = 15093053680
    
CharacterSettings.Hats = {
    1125510,
    439946249
}

CharacterSettings.Torso = {
    80747582883534
}

CharacterSettings.Animations = {
    Idle = 619535834,
    Run = 619536621,
    Walk = 619537468,
    Fall = 658831500,
    Jump = 658832070
}

return CharacterSettings
]])
end

--// Services
local Players = cloneref(game:GetService("Players"))
local RunService = cloneref(game:GetService("RunService"))
local ReplicatedStorage = cloneref(game:GetService("ReplicatedStorage"))
local UserInputService = cloneref(game:GetService("UserInputService"))
local Lighting = cloneref(game:GetService("Lighting"))
local CoreGui = cloneref(game:GetService("CoreGui"))
local HttpService = cloneref(game:GetService("HttpService"))

--// Client
local Client = Players.LocalPlayer
local Camera = workspace.CurrentCamera
local Mouse = Client:GetMouse()

--// Assets
local BodyClone = game:GetObjects("rbxassetid://8246626421")[1]; BodyClone.Humanoid:Destroy(); BodyClone.Head.Face:Destroy(); BodyClone.Parent = Workspace; BodyClone.HumanoidRootPart.Velocity = Vector3.new(); BodyClone.HumanoidRootPart.CFrame = CFrame.new(9999,9999,9999); BodyClone.HumanoidRootPart.Transparency = 1; BodyClone.HumanoidRootPart.CanCollide = false for i,v in pairs(BodyClone:GetChildren()) do if v:IsA("BasePart") or v:IsA("MeshPart") then v.CanCollide = false end end
local BodyCloneHighlight = Instance.new("Highlight"); BodyCloneHighlight.Enabled = true; BodyCloneHighlight.DepthMode = Enum.HighlightDepthMode.AlwaysOnTop; BodyCloneHighlight.FillColor = Library.Theme.Accent; BodyCloneHighlight.OutlineColor = Color3.fromRGB(0, 0, 0); BodyCloneHighlight.Adornee = BodyClone; BodyCloneHighlight.OutlineTransparency = 0.2; BodyCloneHighlight.FillTransparency = 0.5; BodyCloneHighlight.Parent = BodyClone
local TargetHighlight = Instance.new("Highlight"); TargetHighlight.Enabled = true; TargetHighlight.Parent = CoreGui; TargetHighlight.FillColor = Library.Theme.Accent; TargetHighlight.OutlineColor = Library.Theme.Accent; TargetHighlight.FillTransparency = 0.2

local Themes = {
    Default = {1, [[{"Outline":"000000","Accent":"5d3e98","LightText":"ffffff","DarkText":"afafaf","LightContrast":"1e1e1e","CursorOutline":"0a0a0a","DarkContrast":"141414","TextBorder":"000000","Inline":"323232"}]]},
    Abyss = {2, [[{"Outline":"0a0a0a","Accent":"8c87b4","LightText":"ffffff","DarkText":"afafaf","LightContrast":"1e1e1e","CursorOutline":"141414","DarkContrast":"141414","TextBorder":"0a0a0a","Inline":"2d2d2d"}]]},
    Fatality = {3, [[{"Outline":"0f0f28","Accent":"f00f50","LightText":"c8c8ff","DarkText":"afafaf","LightContrast":"231946","CursorOutline":"0f0f28","DarkContrast":"191432","TextBorder":"0a0a0a","Inline":"322850"}]]},
    Neverlose = {4, [[{"Outline":"000005","Accent":"00b4f0","LightText":"ffffff","DarkText":"afafaf","LightContrast":"000f1e","CursorOutline":"0f0f28","DarkContrast":"050514","TextBorder":"0a0a0a","Inline":"0a1e28"}]]},
    Aimware = {5, [[{"Outline":"000005","Accent":"c82828","LightText":"e8e8e8","DarkText":"afafaf","LightContrast":"2b2b2b","CursorOutline":"191919","DarkContrast":"191919","TextBorder":"0a0a0a","Inline":"373737"}]]},
    Youtube = {6, [[{"Outline":"000000","Accent":"ff0000","LightText":"f1f1f1","DarkText":"aaaaaa","LightContrast":"232323","CursorOutline":"121212","DarkContrast":"0f0f0f","TextBorder":"121212","Inline":"393939"}]]},
    Gamesense = {7, [[{"Outline":"000000","Accent":"a7d94d","LightText":"ffffff","DarkText":"afafaf","LightContrast":"171717","CursorOutline":"141414","DarkContrast":"0c0c0c","TextBorder":"141414","Inline":"282828"}]]},
    Onetap = {8, [[{"Outline":"000000","Accent":"dda85d","LightText":"d6d9e0","DarkText":"afafaf","LightContrast":"2c3037","CursorOutline":"000000","DarkContrast":"1f2125","TextBorder":"000000","Inline":"4e5158"}]]},
    Entropy = {9, [[{"Outline":"0a0a0a","Accent":"81bbe9","LightText":"dcdcdc","DarkText":"afafaf","LightContrast":"3d3a43","CursorOutline":"000000","DarkContrast":"302f37","TextBorder":"000000","Inline":"4c4a52"}]]},
    Interwebz = {10, [[{"Outline":"1a1a1a","Accent":"c9654b","LightText":"fcfcfc","DarkText":"a8a8a8","LightContrast":"291f38","CursorOutline":"1a1a1a","DarkContrast":"1f162b","TextBorder":"000000","Inline":"40364f"}]]},
    Dracula = {11, [[{"Outline":"202126","Accent":"9a81b3","LightText":"b4b4b8","DarkText":"88888b","LightContrast":"2a2c38","CursorOutline":"202126","DarkContrast":"252730","TextBorder":"2a2c38","Inline":"3c384d"}]]},
    Spotify = {12, [[{"Outline":"0a0a0a","Accent":"1ed760","LightText":"d0d0d0","DarkText":"949494","LightContrast":"181818","CursorOutline":"000000","DarkContrast":"121212","TextBorder":"000000","Inline":"292929"}]]},
    Sublime = {13, [[{"Outline":"000000","Accent":"ff9800","LightText":"e8ffff","DarkText":"d3d3c2","LightContrast":"32332d","CursorOutline":"000000","DarkContrast":"282923","TextBorder":"000000","Inline":"484944"}]]},
    Vape = {14, [[{"Outline":"0a0a0a","Accent":"26866a","LightText":"dcdcdc","DarkText":"afafaf","LightContrast":"1f1f1f","CursorOutline":"000000","DarkContrast":"1a1a1a","TextBorder":"000000","Inline":"363636"}]]},
    Neko = {15, [[{"Outline":"000000","Accent":"d21f6a","LightText":"ffffff","DarkText":"afafaf","LightContrast":"171717","CursorOutline":"0a0a0a","DarkContrast":"131313","TextBorder":"000000","Inline":"2d2d2d"}]]},
    Corn = {16, [[{"Outline":"000000","Accent":"ff9000","LightText":"dcdcdc","DarkText":"afafaf","LightContrast":"252525","CursorOutline":"000000","DarkContrast":"191919","TextBorder":"000000","Inline":"333333"}]]},
    Minecraft = {17, [[{"Outline":"000000","Accent":"27ce40","LightText":"ffffff","DarkText":"d7d7d7","LightContrast":"333333","CursorOutline":"000000","DarkContrast":"262626","TextBorder":"000000","Inline":"333333"}]]}
}

--// Tables
local Script = {
    Targeting = {Target = nil},

    Client = {
        RootPart = nil,
        Humanoid = nil,
        Character = nil,
        Tool = nil
    },

    Data = {
        Players = {},
        Esp = {},

        Desync = {},
        Prefiretick = 0,
        DestroyHeight = workspace.FallenPartsDestroyHeight
    },

    Toggles = {
        Targeting = false,
        ServerDesync = false,
        VelocitySpoofer = false,
        Fly = false,
        CFrame = false,
        KeybindShoot = false
    },

    Animation = {
        Animations = {
            ["Floss"] = "10714340543",
            ["Flex Walk"] = "15505459811",
            ["HUGO Let's Drive!"] = "17360699557"
        },

        AnimationObject = nil,
        Animation = nil
    },

    Functions = {},
    Connections = {},
    Hooks = {},
    Debounces = {},
    Drawings = {}
}

local UI = {
    Combat = {
        Targeting = {
            Enabled = false,
            Sticky = false,
            Hitpoints = {"Head"}
        },

        Legitbot = {
            Enabled = false,
            PredictionEnabled = false,
            PredictionValue = 0.095,
            Smoothness = 2,
            JumpOffsetEnabled = false,
            JumpOffsetValue = 0
        },

        SilentAim = {
            Enabled = false,
            ForceHit = false,
            DoubleTap = false,
            DoubleTapMode = "Activate",
            Manipulation = false,
            Prefire = false,
            PrefireSeconds = 3
        },

        Fov = {
            StickTarget = false,
            StickBarrel = false
        },

        TargetVisuals = {
            Highlight = false,
            TargetText = false
        },

        Checks = {
            Knocked = false,
            Raycast = false,
            Friend = false,
            Forcefield = false
        }
    },

    AntiAim = {
        ServerDesync = {
            Enabled = false,
            Mode = "Custom",

            Custom = {
                X = 1,
                Y = 1,
                Z = 1,

                XX = 1,
                YY = 1, 
                ZZ = 1
            }
        },

        VelocitySpoofer = {
            Enabled = false,
            Mode = "Random",

            Custom = {
                X = 1,
                Y = 1,
                Z = 1,

                MinX = 1,
                MaxX = 1,
                MinY = 1,
                MaxY = 1,
                MinZ = 1,
                MaxZ = 1
            }
        }
    },

    Misc = {
        Movement = {
            Fly = {
                Enabled = false,
                Speed = 50
            },

            CFrame = {
                Enabled = false,
                Speed = 1
            }
        },

        Client = {
            AntiJumpCooldown = false,
            AntiSlow = false,
            FaceBackwards = false,
            AntiStomp = false,

            AvatarChanger = {
                LoadOnDeath = false,
                Name = ""
            },

            Animation = {
                Selected = "Floss",
                Speed = 1
            }
        }
    },

    -- 🔥 VISUALS mới thêm vào đây
    Visuals = {
        BulletTracer = {
		    Enabled = false,
		    SelectedTexture = "rbxassetid://12781852245",
		    TextureID = "rbxassetid://12781852245",
		    Color = Color3.fromRGB(155, 125, 175),
		    Size = 0.4,
		    Transparency = 0,
		    TimeAlive = 2
        }
    }
}

local TweenService = game:GetService("TweenService")
local Workspace = game:GetService("Workspace")
local function bullettracerlol(startPos, endPos)
    local startPart = Instance.new("Part")
    startPart.Name = "BulletStart"
    startPart.Anchored = true
    startPart.CanCollide = false
    startPart.Transparency = 1
    startPart.Size = Vector3.new(0.2, 0.2, 0.2)
    startPart.Material = Enum.Material.ForceField
    startPart.Color = Color3.new(1, 0, 0)
    startPart.Transparency = 1
    startPart.CanTouch = false
    startPart.CanQuery = false
    startPart.Massless = true
    startPart.CollisionGroupId = 0
    startPart.Position = startPos
    startPart.Parent = Workspace

    local endPart = Instance.new("Part")
    endPart.Name = "BulletEnd"
    endPart.Anchored = true
    endPart.CanCollide = false
    endPart.Size = Vector3.new(0.2, 0.2, 0.2)
    endPart.Material = Enum.Material.ForceField
    endPart.Color = Color3.new(1, 0, 0)
    endPart.Transparency = 1
    endPart.CanTouch = false
    endPart.CanQuery = false
    endPart.Massless = true
    endPart.CollisionGroupId = 0
    endPart.Position = endPos
    endPart.Parent = Workspace

    local beam = Instance.new("Beam")
    beam.Attachment0 = Instance.new("Attachment", startPart)
    beam.Attachment1 = Instance.new("Attachment", endPart)
    beam.Parent = startPart
    beam.FaceCamera = true
    beam.Color = ColorSequence.new(UI.Visuals.BulletTracer.Color)
    beam.Texture = UI.Visuals.BulletTracer.TextureID
    beam.LightEmission = 1
    beam.Transparency = NumberSequence.new(UI.Visuals.BulletTracer.Transparency)
    beam.Width0 = UI.Visuals.BulletTracer.Size
    beam.Width1 = UI.Visuals.BulletTracer.Size

    task.delay(UI.Visuals.BulletTracer.TimeAlive, function()
        if beam and beam.Parent then
            local tweenInfo = TweenInfo.new(0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out)
            local tween = TweenService:Create(beam, tweenInfo, { Width0 = 0, Width1 = 0 })
            tween:Play()
            
            tween.Completed:Wait()
        end

        if startPart and startPart.Parent then startPart:Destroy() end
        if endPart and endPart.Parent then endPart:Destroy() end
        if beam and beam.Parent then beam:Destroy() end
    end)

    return startPart, endPart, beam
end
local possibleRemotes = { "MAINEVENT", "MainEvent", "Remote", "Bullets", "MainRemotes", "Packages" }
local Services = {

    ReplicatedStorage = game:GetService("ReplicatedStorage"),

}
local function getMainRemote()
    if Services.ReplicatedStorage:FindFirstChild("MainEvent") then return Services.ReplicatedStorage.MainEvent end
    if Services.ReplicatedStorage:FindFirstChild("MAINEVENT") then return Services.ReplicatedStorage.MAINEVENT end
    if Services.ReplicatedStorage:FindFirstChild("Remote") then return Services.ReplicatedStorage.Remote end
    if Services.ReplicatedStorage:FindFirstChild("Bullets") then return Services.ReplicatedStorage.Bullets end
    
    local mainRemotes = Services.ReplicatedStorage:FindFirstChild("MainRemotes")
    if mainRemotes and mainRemotes:FindFirstChild("MainRemoteEvent") then return mainRemotes.MainRemoteEvent end
    
    local packages = Services.ReplicatedStorage:FindFirstChild("Packages")
    if packages then
        local knit = packages:FindFirstChild("Knit")
        if knit then
            local toolService = knit.Services:FindFirstChild("ToolService")
            if toolService and toolService.RE:FindFirstChild("UpdateAim") then
                return toolService.RE.UpdateAim
            end
        end
    end
    return nil
end
local MainRemote = getMainRemote()
local OldNamecall
OldNamecall = hookmetamethod(game, "__namecall", function(Self, ...)
    local Args = {...}
    local Method = getnamecallmethod()

    if Method == "FireServer" and Self == MainRemote and Args[1] == "ShootGun" and UI.Visuals.BulletTracer.Enabled then
        local Handle = Args[2]  -- Tool Handle
        local OriginPos = Args[3]  -- Handle.Position
        local HitPos = Args[4]     -- Target Hit Position

        if Handle and OriginPos and HitPos then
            task.spawn(function()
                bullettracerlol(OriginPos, HitPos)
            end)
        end
    end

    return OldNamecall(Self, ...)
end)
matcha = {
    Version = "2.0.1",
    Names = {
        "Ratzzzzz",
        "$$$$$$$$",
        "zzzzzzzzzzzzzzz",
        "zzzzzz$ZZZZZZ$Z$Z$Z$Z$Z$Z$",
        "$$$$zzzzzzzzzzzzzzzzz$$$$",
        "sss$$$$s",
        "undetek",
        "obese.vip",
        "headshot.cc",
        "halooo",
        "matcha.lol",
        "ratted",
        "silentaim.win",
        "hooked.lol",
        "ghostclient",
        "desynced.gg",
        "undetected.lol",
        "chat.gpt",
        "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$",
        "R444aSasdateddd",
        "txriswwareee4$$$",
        "txriswwareee4$$$",
        "!!1!1!"
    },
    Configs = {},
    Characters = {}
}

--// Funcs
local Random = math.random
local FindFirstChild = game.FindFirstChild
local GetMousePosition = function()
    return UserInputService:GetMouseLocation()
end
local ViewportSize = Camera.ViewportSize

do --[[ Functions ]]--
    do --[[ Logic ]]--
        Script.Functions.CreateConnection = LPH_NO_VIRTUALIZE(function(Connection, Function)
            table.insert(Script.Connections, Connection:Connect(Function))
        end)

        Script.Functions.Drawing = LPH_NO_VIRTUALIZE(function(Type, Options)
            local Object = Drawing.new(Type)

            for Option, Value in pairs(Options) do
                Object[Option] = Value
            end

            return Object
        end)

        Script.Functions.ClientChecks = LPH_NO_VIRTUALIZE(function()
            if not Script.Client.RootPart or not Script.Client.Character or not Script.Client.Humanoid then return false end

            return true 
        end)

        Script.Functions.TargetExists = function()
            if not Script.Targeting.Target or not Script.Targeting.Target.Character then return false end

            return true
        end

        Script.Functions.CalculateManipulation = function(Origin, Target)
            local FinalOrigin = Origin * CFrame.new(0, 0, 0, 1, 0, 0, 0, 0, 1, 0, -1, 0)
            return FinalOrigin:ToObjectSpace(Target):inverse();
        end
		
        Script.Functions.Manipulation = function()
            if not Script.Functions.ClientChecks() then return end
            -- broken rip
        end

        Script.Functions.ResetTargetVisuals = function()
            TargetHighlight.Adornee = nil
        end

        Script.Functions.KeybindShoot = function()
            if not Script.Client.Tool then return end
            Script.Toggles.KeybindShoot = true
            task.wait(0.15)
            Script.Client.Tool:Activate()
            task.wait(0.25)
            Script.Toggles.KeybindShoot = false
        end

        Script.Drawings.Fov = Script.Functions.Drawing("Circle", {Radius = 120, Thickness = 1, ZIndex = 10000, Visible = false, Filled = false, Color = Library.Theme.Accent})
        Script.Drawings.TargetName = Script.Functions.Drawing("Text", {Size = 13, Font = 2, ZIndex = 10000, Visible = false, Outline = true, Color = Color3.fromRGB(255, 255, 255)})
        Script.Drawings.DesyncStatus = Script.Functions.Drawing("Text", {Size = 13, Text = "Desync Status: false", Position = Vector2.new(ViewportSize.X / 2, ViewportSize.Y / 2), Center = true, Font = 2, ZIndex = 10000, Visible = false, Outline = true, Color = Color3.fromRGB(255, 255, 255)})
        Script.Drawings.VelocityStatus = Script.Functions.Drawing("Text", {Size = 13, Text = "Velocity Status: false", Position = Vector2.new(ViewportSize.X / 2, ViewportSize.Y / 1.9), Center = true, Font = 2, ZIndex = 10000, Visible = false, Outline = true, Color = Color3.fromRGB(255, 255, 255)})
        Script.Drawings.FilledFov = Script.Functions.Drawing("Circle", {Radius = 120, Thickness = 0, ZIndex = 10000, Visible = false, Filled = true, Color = Library.Theme.Accent})
    end

    do --[[ Targeting ]]--
        Script.Functions.RaycastCheck = LPH_NO_VIRTUALIZE(function(Destination, Ignore)
            local Origin = Camera.CFrame.p
            local CheckRay = Ray.new(Origin, Destination - Origin)
            local Hit = workspace:FindPartOnRayWithIgnoreList(CheckRay, Ignore)

            return Hit == nil
        end)
        
        Script.Functions.RunChecks = function(Player, Character)
            if not Player then return false end
            if not Character then return false end
            if not Character['BodyEffects'] then return false end

            if UI.Combat.Checks.Knocked and Character['BodyEffects']['K.O'].Value == true then
                return false
            end

            if UI.Combat.Checks.Raycast and not Script.Functions.RaycastCheck(Character.HumanoidRootPart.Position, {Client, Character, BodyClone, Camera}) then
                return false
            end

            if UI.Combat.Checks.Friend and Player:IsFriendsWith(Client.UserId) then
                return false
            end

            if UI.Combat.Checks.Forcefield and Character:FindFirstChildWhichIsA("ForceField") then
                return false
            end

            return true
        end
        
        Script.Functions.GetTarget = LPH_NO_VIRTUALIZE(function(Radius)
            local Target = nil
            local MaximumDistance = math.huge

            for _, Player in pairs(Script.Data.Players) do
                if Player == Client then
                    continue
                end

                if not Player.Character then
                    continue
                end

                local HumanoidRootPart = FindFirstChild(Player.Character, "HumanoidRootPart")
                if (not HumanoidRootPart) then
                    continue
                end

                local Position, OnScreen = Camera:WorldToViewportPoint(HumanoidRootPart.Position)
                if not OnScreen then continue end

                local Magnitude = (Vector2.new(Position.X, Position.Y) - GetMousePosition()).Magnitude

                if Magnitude > Radius then
                    continue
                end
                if not Script.Functions.RunChecks(Player, Player.Character) then continue end

                if Magnitude <= MaximumDistance then
                    Target = Player
                    MaximumDistance = Magnitude
                end
            end
            return Target
        end)

        Script.Functions.GetPart = LPH_NO_VIRTUALIZE(function(Character)
            local Hitpart = nil
            local MaximumDistance = math.huge
            
            for _, Part in pairs(Character:GetChildren()) do
                if (Part:IsA("BasePart") or Part:IsA("MeshPart") or Part:IsA("Part")) and table.find(UI.Combat.Targeting.Hitpoints, Part.Name) then
                    local Position, OnScreen = Camera:WorldToViewportPoint(Part.Position)
                    if OnScreen then
                        local Magnitude = (Vector2.new(Position.X, Position.Y) - GetMousePosition()).Magnitude
                        if Magnitude <= MaximumDistance then
                            Hitpart = Part.Name
                            MaximumDistance = Magnitude
                        end
                    end
                end
            end
            
            return Hitpart
        end)

        Script.Functions.SetTarget = LPH_NO_VIRTUALIZE(function(Radius)
            Script.Targeting.Target = Script.Functions.GetTarget(Radius or math.huge)

            TargetHighlight.Adornee = UI.Combat.TargetVisuals.Highlight and Script.Targeting.Target and Script.Targeting.Target.Character or nil
        end)
        
        Script.Functions.Teleport = function(Player)
            if not Script.Functions.ClientChecks() then return end
            if not Player.Character or not Player.Character:FindFirstChild("HumanoidRootPart") then return end

            Script.Client.RootPart.CFrame = Player.Character.HumanoidRootPart.CFrame + Vector3.new(0, 5, 0)
        end

        Script.Functions.GetShootingPosition = function(Character)
            local Hitpart = Character[Script.Functions.GetPart(Character)]
            return CFrame.new(Hitpart.Position)
        end

        Script.Functions.GetTargetPart = LPH_NO_VIRTUALIZE(function(Character)
            if not Character then return end
            local Hitpart = Character[Script.Functions.GetPart(Character)]
            return Hitpart
        end)

        Script.Functions.DoubleTap = function(Tool, Cooldown)
            if UI.Combat.SilentAim.DoubleTapMode == "Activate" then
                task.wait(Cooldown + 0.002)
                Tool:Activate()
            elseif UI.Combat.SilentAim.DoubleTapMode == "Secret" then
                task.wait(Cooldown + 0.05)
                if not Script.Functions.TargetExists() then
                    return 
                end
                local args = {
                    "Shoot",
                    {
                        {
                            [1] = {
                                ["Instance"] = Script.Targeting.Target.Character['Head'],
                                ["Normal"] = Vector3.new(0.9937344193458557, 0.10944880545139313, -0.022651424631476402),
                                ["Position"] = Vector3.new(-141.78562927246094, 33.89368438720703, -365.6424865722656)
                            },
                            [2] = {
                                ["Instance"] = Script.Targeting.Target.Character['Head'],
                                ["Normal"] = Vector3.new(0.9937344193458557, 0.10944880545139313, -0.022651424631476402),
                                ["Position"] = Vector3.new(-141.78562927246094, 33.89368438720703, -365.6424865722656)
                            },
                            [3] = {
                                ["Instance"] = Script.Targeting.Target.Character['Head'],
                                ["Normal"] = Vector3.new(0.9937343597412109, 0.10944879800081253, -0.022651422768831253),
                                ["Position"] = Script.Targeting.Target.Character['Head'].Position 
                            },
                            [4] = {
                                ["Instance"] = Script.Targeting.Target.Character['Head'],
                                ["Normal"] = Vector3.new(0.9937344193458557, 0.10944880545139313, -0.022651424631476402),
                                ["Position"] = Script.Targeting.Target.Character['Head'].Position 
                            },
                            [5] = {
                                ["Instance"] = Script.Targeting.Target.Character['Head'],
                                ["Normal"] = Vector3.new(0.9937344193458557, 0.10944880545139313, -0.022651424631476402),
                                ["Position"] = Vector3.new(-141.79481506347656, 34.033607482910156, -365.369384765625)
                            }
                        },
                        {
                            [1] = {
                                ["thePart"] = Script.Targeting.Target.Character['Head'],
                                ["theOffset"] = CFrame.new(0, 0, 0)
                            },
                            [2] = {
                                ["thePart"] = Script.Targeting.Target.Character['Head'],
                                ["theOffset"] = CFrame.new(0, 0, 0)
                            },
                            [3] = {
                                ["thePart"] = Script.Targeting.Target.Character['Head'],
                                ["theOffset"] = CFrame.new(0, 0, 0)
                            },
                            [4] = {
                                ["thePart"] = Script.Targeting.Target.Character['Head'],
                                ["theOffset"] = CFrame.new(0, 0, 0)
                            },
                            [5] = {
                                ["thePart"] = Script.Targeting.Target.Character['Head'],
                                ["theOffset"] = CFrame.new(0, 0, 0)
                            }
                        },
                        Client.Character.Head.Position,
                        Client.Character.Head.Position,
                        workspace:GetServerTimeNow()
                    }
                }

                MainRemote:FireServer(unpack(args))
            end
        end
    end

    do --[[ Extras ]]--  
        if isfolder("matcha/Configs") then
            for i, v in pairs(listfiles("matcha/Configs")) do
                local filename = v:match("^.+[\\/](.+)$")
                local nameWithoutExtension = filename:match("(.+)%..+$")
                table.insert(matcha.Configs, nameWithoutExtension)
            end
        else
            makefolder("matcha/Configs")
        end

        if isfolder("matcha/Characters") then
            for i, v in pairs(listfiles("matcha/Characters")) do
                local filename = v:match("^.+[\\/](.+)$")
                local nameWithoutExtension = filename:match("(.+)%..+$")
                table.insert(matcha.Characters, nameWithoutExtension)
            end
        else
            makefolder("matcha/Characters")
        end
    end

    do --[[ Essentials ]]--
        Script.Functions.WeldParts = function(Part0, Part1, C0, C1)
            local Weld = Instance.new("Weld")
            Weld.Part0 = Part0
            Weld.Part1 = Part1
            Weld.C0 = C0
            Weld.C1 = C1
            Weld.Parent = Part0
            return Weld
        end

        Script.Functions.FindAttachment = function(RootPart, Name)
            for _, Descendant in pairs(RootPart:GetDescendants()) do
                if Descendant:IsA("Attachment") and Descendant.Name == Name then
                    return Descendant
                end
            end
        end

        Script.Functions.AddAccessory = function(AccessoryId, ParentPart)
            local Accessory = game:GetObjects("rbxassetid://" .. tostring(AccessoryId))[1]
            local Character = Client.Character

            Accessory.Parent = game.Workspace

            local Handle = Accessory:FindFirstChild("Handle")
            if Handle then
                local Attachment = Handle:FindFirstChildOfClass("Attachment")
                if Attachment then
                    local ParentAttachment = Script.Functions.FindAttachment(ParentPart, Attachment.Name)
                    if ParentAttachment then
                        Script.Functions.WeldParts(ParentPart, Handle, ParentAttachment.CFrame, Attachment.CFrame)
                    end
                else
                    local Parent = Character:FindFirstChild(ParentPart.Name)
                    if Parent then
                        local AttachmentPoint = Accessory.AttachmentPoint
                        Script.Functions.WeldParts(Parent, Handle, CFrame.new(0, 0.5, 0), AttachmentPoint.CFrame)
                    end
                end
            end

            Accessory.Parent = Character
        end

        Script.Functions.AddClothingToCharacter = function(ClothingId)
            local Accessory = game:GetObjects("rbxassetid://" .. tostring(ClothingId))[1]
            local Character = Client.Character

            Accessory.Parent = Character
        end

        Script.Functions.AddAnimationsToCharacter = function(AnimationId)
            local Accessory = game:GetObjects("rbxassetid://" .. tostring(AnimationId))[1]:FindFirstChildOfClass("StringValue")
            local Character = Client.Character

            Accessory.Parent = Character:WaitForChild("Animate")
        end

        Script.Functions.GrabCustomHead = function(HeadId)
            local Accessoryid = game:GetObjects("rbxassetid://" .. tostring(HeadId))[1].MeshId
            local AccessoryTextureId = game:GetObjects("rbxassetid://" .. tostring(HeadId))[1].TextureId
            local Character = Client.Character

            Character.Head.MeshId = Accessoryid
            Character.Head.TextureID = AccessoryTextureId
        end

        Script.Functions.ApplyCharacter = function(Config, Character)
            task.wait(1.5)

            -- Destroy old fuck accesories!!
            for _, Accessory in pairs(Character:GetDescendants()) do
                if Accessory:IsA("Accessory") then
                    Accessory:Destroy()
                end
            end

            for _, AccessoryId in ipairs(Config.Hats) do
                Script.Functions.AddAccessory(AccessoryId, Character.Head)
            end

            for _, AccessoryId in ipairs(Config.Torso) do
                Script.Functions.AddAccessory(AccessoryId, Character:FindFirstChild("UpperTorso") or Character:FindFirstChild("Torso"))
            end

            if Character:FindFirstChild("Pants") then
                Character:FindFirstChild("Pants"):Destroy()
            end
            if Character:FindFirstChild("Shirt") then
                Character:FindFirstChild("Shirt"):Destroy()
            end

            Script.Functions.AddClothingToCharacter(Config.Pants)
            Script.Functions.AddClothingToCharacter(Config.Shirt)

            local Animate = Character:WaitForChild("Animate", 2)
            Animate.fall:Destroy()
            Animate.jump:Destroy()
            Animate.idle:Destroy()
            Animate.walk:Destroy()
            Animate.run:Destroy()

            task.wait(0.1)

            Script.Functions.AddAnimationsToCharacter(Config.Animations.Fall)
            Script.Functions.AddAnimationsToCharacter(Config.Animations.Jump)
            Script.Functions.AddAnimationsToCharacter(Config.Animations.Walk)
            Script.Functions.AddAnimationsToCharacter(Config.Animations.Run)
            Script.Functions.AddAnimationsToCharacter(Config.Animations.Idle)


            Script.Functions.GrabCustomHead(Config.Head)
        end
    end
    
    do --[[ Client ]]--
        Script.Functions.LoadAvatar = function(ConfigName)
            if not Script.Functions.ClientChecks() then return end
            local CharacterConfig = readfile(("matcha/Characters/%s"):format(ConfigName .. ".Character"))
            local CharacterSettings = loadstring(CharacterConfig)()

            Script.Functions.ApplyCharacter(CharacterSettings, Script.Client.Character)
        end

        Script.Functions.LoadAnimation = function(AnimationId)
            if not Script.Functions.ClientChecks() then return end

            Script.Animation.AnimationObject = Instance.new('Animation')
            Script.Animation.AnimationObject.AnimationId = "rbxassetid://"..tostring(AnimationId)
            Script.Animation.AnimationObject.Parent = Client.Character

            Script.Animation.Animation = Script.Client.Humanoid:LoadAnimation(Script.Animation.AnimationObject)
            Script.Animation.Animation.Priority = Enum.AnimationPriority.Action4

            Script.Animation.Animation.Looped = true
            Script.Animation.Animation:Play()
        end

        Script.Functions.ForceReset = function()
            Script.Client.Humanoid:ChangeState(15)
            task.wait()
            Script.Client.Humanoid:ChangeState(16)
            Script.Client.Humanoid:ChangeState(0)
        end
    end
end 

---------------------------------------[[ Connections ]]---------------------------------------
do --[[ Connections ]]--
    do --[[ Players ]]--
        for _, Player in pairs(Players:GetPlayers()) do
            table.insert(Script.Data.Players, Player)
        end

        Script.Functions.CreateConnection(Players.PlayerAdded, function(Player)
            table.insert(Script.Data.Players, Player)
        end)

        Script.Functions.CreateConnection(Players.PlayerRemoving, function(Player)
            local PlayerIndex = table.find(Script.Data.Players, Player)
            table.remove(Script.Data.Players, PlayerIndex)
        end)
    end

    do --[[ Chat ]]--
        --
    end

    do --[[ Client ]]--
        Script.Client.Character = Client.Character or nil
        Script.Client.RootPart = Client.Character:FindFirstChild("HumanoidRootPart") or nil
        Script.Client.Humanoid = Client.Character:FindFirstChildOfClass("Humanoid") or nil
        Script.Client.Tool = Client.Character:FindFirstChildOfClass("Tool") or nil

        Script.Functions.CreateConnection(Client.CharacterAdded, function()
            Script.Client.Character = Client.Character or nil
            Script.Client.RootPart = Client.Character:WaitForChild("HumanoidRootPart") or nil
            Script.Client.Humanoid = Client.Character:WaitForChild("Humanoid") or nil

            if UI.Misc.Client.AvatarChanger.LoadOnDeath then
                Script.Functions.LoadAvatar(UI.Misc.Client.AvatarChanger.Name)
            end

            Script.Connections['Child Added Connection'] = Script.Client.Character.ChildAdded:Connect(function(Child)
                if Child:IsA("Tool") and Child:FindFirstChild("GunData") then
                    Script.Client.Tool = Child
                    local Data = require(Script.Client.Tool.GunData)

                    Script.Connections['Tool Activated Connection'] = Mouse.Button1Down:Connect(function()
                        if UI.Combat.SilentAim.DoubleTap and Script.Client.Tool then
                            Script.Functions.DoubleTap(Script.Client.Tool, Data.cooldown)
                        end
                    end)
                end

                if Child:IsA("ForceField") then
                    Script.Data.Prefiretick = tick()
                end
            end)

            Script.Connections['Child Removed Connection'] = Script.Client.Character.ChildRemoved:Connect(function(Child)
                if Child:IsA("Tool") then
                    Script.Client.Tool = nil

                    Script.Connections['Tool Activated Connection']:Disconnect()
                    Script.Connections['Tool Activated Connection'] = nil
                end
            end)
        end)

        if not Script.Connections['Child Added Connection'] or not Script.Connections['Child Removed Connection'] then
            Script.Connections['Child Added Connection'] = Script.Client.Character.ChildAdded:Connect(function(Child)
                if Child:IsA("Tool") and Child:FindFirstChild("GunData") then
                    Script.Client.Tool = Child
                    local Data = require(Script.Client.Tool.GunData)

                    Script.Connections['Tool Activated Connection'] = Mouse.Button1Down:Connect(function()
                        if UI.Combat.SilentAim.DoubleTap and Script.Client.Tool then
                            Script.Functions.DoubleTap(Script.Client.Tool, Data.cooldown)
                        end
                    end)
                end

                if Child:IsA("ForceField") then
                    Script.Data.Prefiretick = tick()
                end
            end)

            Script.Connections['Child Removed Connection'] = Script.Client.Character.ChildRemoved:Connect(function(Child)
                if Child:IsA("Tool") then
                    Script.Client.Tool = nil

                    Script.Connections['Tool Activated Connection']:Disconnect()
                    Script.Connections['Tool Activated Connection'] = nil
                end
            end)
        end


        Script.Functions.CreateConnection(Client.CharacterRemoving, function(Child)
            Script.Client.RootPart = nil
            Script.Client.Character = nil
            Script.Client.Humanoid = nil
            Script.Client.Tool = nil

            Script.Connections['Child Added Connection']:Disconnect()
            Script.Connections['Child Removed Connection']:Disconnect()
        end)
    end
end 

---------------------------------------[[ Framework ]]---------------------------------------
local V2New = Vector2.new
local WorldToViewport = Camera.WorldToViewportPoint

Script.Functions.CreateConnection(RunService.Heartbeat, function()
    local Tool = Script.Client.Tool
    local Handle = Tool and Tool:FindFirstChild("Handle")
    local ShootGui = Handle and Handle:FindFirstChild("ShootBBGUI")
    local StudsOffset = ShootGui and ShootGui.StudsOffsetWorldSpace
    local HandleCFrame = Handle and Handle.CFrame

    local BarrelWorldPosition
    if HandleCFrame and StudsOffset then
        BarrelWorldPosition =
            HandleCFrame.Position
            - HandleCFrame.LookVector * StudsOffset.Z
            + HandleCFrame.UpVector * StudsOffset.Y
            - HandleCFrame.RightVector * math.abs(StudsOffset.X)
    end

    local Target = Script.Targeting.Target
    local TargetHRP = Target and Target.Character and Target.Character:FindFirstChild("HumanoidRootPart")

    local TargetScreenPosition
    if TargetHRP then
        TargetScreenPosition, OnScreen = WorldToViewport(Camera, TargetHRP.Position)
    end


    BarrelScreenPosition = BarrelWorldPosition and WorldToViewport(Camera, BarrelWorldPosition)

    local StickTarget = UI.Combat.Fov.StickTarget
    local StickBarrel = UI.Combat.Fov.StickBarrel

    local FovPosition
    if Target and StickTarget and TargetScreenPosition then
        FovPosition = V2New(TargetScreenPosition.X, TargetScreenPosition.Y)
    end
    if (not FovPosition) and StickBarrel and BarrelScreenPosition then
        FovPosition = V2New(BarrelScreenPosition.X, BarrelScreenPosition.Y)
    end
    if not FovPosition then
        FovPosition = GetMousePosition()
    end

    local DrawFov = Script.Drawings.Fov
    local DrawFilledFov = Script.Drawings.FilledFov
    local DrawTargetName = Script.Drawings.TargetName

    DrawFov.Position = FovPosition
    DrawFilledFov.Position = FovPosition

    DrawTargetName.Visible = UI.Combat.TargetVisuals.TargetText and OnScreen and Script.Targeting.Target and true or false
    DrawTargetName.Position = TargetScreenPosition and V2New(TargetScreenPosition.X, TargetScreenPosition.Y) or V2New(0, 0)
    DrawTargetName.Text = Target and "$$$$ " .. Target.Name .. " $$$$" or ""
end)
local RunService = game:GetService("RunService")
local Players = game:GetService("Players")
local Camera = workspace.CurrentCamera
local LocalPlayer = Players.LocalPlayer

RunService.RenderStepped:Connect(function()
    if not UI.Combat.Legitbot.Enabled or not LocalPlayer.Character then return end
    
    local target = Script.Targeting.Target and Script.Targeting.Target.Character
    if not target then return end
    
    local part = Script.Functions.GetTargetPart(target)
    if not part then return end
    
    local humanoid = target:FindFirstChild("Humanoid")
    if not humanoid then return end

    local pos = part.Position

    -- Prediction
    if UI.Combat.Legitbot.PredictionEnabled then
        pos = pos + (part.AssemblyLinearVelocity * UI.Combat.Legitbot.PredictionValue)
    end

    -- Jump Offset
    if UI.Combat.Legitbot.JumpOffsetEnabled 
       and humanoid:GetState() == Enum.HumanoidStateType.Freefall then
        pos = pos + Vector3.new(0, UI.Combat.Legitbot.JumpOffsetValue, 0)
    end

    -- Goal camera
    local goal = CFrame.lookAt(Camera.CFrame.Position, pos)

    -- Smooth
    local a = UI.Combat.Legitbot.Smoothness
    Camera.CFrame = Camera.CFrame:Lerp(goal, a)
end)


Script.Functions.CreateConnection(RunService.Heartbeat, function(Delta) -- Combat Mainly
    if Script.Toggles.Targeting and not UI.Combat.Targeting.Sticky then
        Script.Functions.SetTarget(Script.Drawings.Fov.Radius)
    end

    if UI.Combat.SilentAim.Prefire and Script.Targeting.Target and Script.Targeting.Target.Character and Script.Client.Tool then
        if (tick() - Script.Data.Prefiretick) >= UI.Combat.SilentAim.PrefireSeconds then
            Script.Client.Tool:Activate()
            Script.Data.Prefiretick = tick()
        end
    end
end)

Script.Functions.CreateConnection(RunService.Heartbeat, function(Delta) -- Desync
    if not UI.AntiAim.ServerDesync.Enabled or not Script.Toggles.ServerDesync then BodyClone:SetPrimaryPartCFrame(CFrame.new(9999,9999,9999)) return end
    if not Script.Functions.ClientChecks() then BodyClone:SetPrimaryPartCFrame(CFrame.new(9999,9999,9999)) return end

    local Desyncs = {
        ["Custom"] = Script.Client.RootPart.CFrame * CFrame.new(UI.AntiAim.ServerDesync.Custom.X, UI.AntiAim.ServerDesync.Custom.Y, UI.AntiAim.ServerDesync.Custom.Z) * CFrame.Angles(UI.AntiAim.ServerDesync.Custom.XX, UI.AntiAim.ServerDesync.Custom.YY, UI.AntiAim.ServerDesync.Custom.ZZ),
        ["Safe Shoot"] = CFrame.new(Script.Client.RootPart.Position - Vector3.new(0, 5, 0)) * CFrame.Angles(Random(0, 360), Random(0, 360), math.rad(180)),
        ['Keybind Shoot'] = Script.Toggles.KeybindShoot and Script.Client.RootPart.CFrame * CFrame.Angles(Random(0, 720), Random(0, 720), Random(0, 720)) or CFrame.new(999999999, 999999999, 999999999) * CFrame.Angles(Random(0, 720), Random(0, 720), Random(0, 720)),
        ["Underground"] = CFrame.new(Script.Client.RootPart.Position - Vector3.new(0, 10, 0)) * CFrame.Angles(0, 0, math.rad(180)),
        ["Mole"] = CFrame.new(Script.Client.RootPart.Position - Vector3.new(0, 10, 0)) * CFrame.Angles(Random(0, 360), Random(0, 360), math.rad(180)),
        ["Moke"] = CFrame.new(Script.Client.RootPart.Position - Vector3.new(0, 15, 0)) * CFrame.Angles(Random(0, 360), Random(0, 360), math.rad(180)),
        ["Mok"] = CFrame.new(Script.Client.RootPart.Position - Vector3.new(0, 20, 0)) * CFrame.Angles(Random(0, 360), Random(0, 360), Random(0, 360)),
        ['Spin'] = Script.Client.RootPart.CFrame * CFrame.Angles(Random(0, 720), Random(0, 720), Random(0, 720)),
        ["Musk"] = math.random(1, 2) == 1 and CFrame.new(999999999, 999999999, 999999999) * CFrame.Angles(Random(0, 720), Random(0, 720), Random(0, 720)) or CFrame.new(Script.Client.RootPart.Position) * CFrame.Angles(Random(0, 720), Random(0, 720), Random(0, 720)),
        ['Tool'] = Script.Client.Tool and Script.Client.RootPart.CFrame * CFrame.Angles(Random(0, 720), Random(0, 720), Random(0, 720)) or CFrame.new(999999999, 999999999, 999999999) * CFrame.Angles(Random(0, 720), Random(0, 720), Random(0, 720))
    }
    
    CFrameDesync = Desyncs[UI.AntiAim.ServerDesync.Mode]

    Script.Data.Desync[1] = Script.Client.RootPart.CFrame
    Script.Client.RootPart.CFrame = CFrameDesync
    BodyClone:SetPrimaryPartCFrame(Script.Client.RootPart.CFrame)
    RunService.RenderStepped:Wait()
    Script.Client.RootPart.CFrame = Script.Data.Desync[1]
end)

Script.Functions.CreateConnection(RunService.Heartbeat, function(Delta) -- Velocity
    if not UI.AntiAim.VelocitySpoofer.Enabled or not Script.Toggles.VelocitySpoofer then BodyClone:SetPrimaryPartCFrame(CFrame.new(9999,9999,9999)) return end

    local Desyncs = {
        ["Custom"] = Vector3.new(UI.AntiAim.VelocitySpoofer.Custom.X, UI.AntiAim.VelocitySpoofer.Custom.Y, UI.AntiAim.VelocitySpoofer.Custom.Z),
        ['Random'] = Vector3.new(math.random(UI.AntiAim.VelocitySpoofer.Custom.MinX, UI.AntiAim.VelocitySpoofer.Custom.MaxX), math.random(UI.AntiAim.VelocitySpoofer.Custom.MinY, UI.AntiAim.VelocitySpoofer.Custom.MaxY), math.random(UI.AntiAim.VelocitySpoofer.Custom.MinZ, UI.AntiAim.VelocitySpoofer.Custom.MaxZ))
    }
    
    SpoofedVelocity = Desyncs[UI.AntiAim.VelocitySpoofer.Mode]

    Script.Data.Desync[2] = Script.Client.RootPart.Velocity
    Script.Client.RootPart.Velocity = SpoofedVelocity
    RunService.RenderStepped:Wait()
    Script.Client.RootPart.Velocity = Script.Data.Desync[2]
end)

Script.Functions.CreateConnection(RunService.Heartbeat, function(Delta) -- Misc Stuff
    if not Script.Functions.ClientChecks() then return end

    local RootPart = Script.Client.RootPart
    local Humanoid = Script.Client.Humanoid

    if Script.Toggles.Fly and UI.Misc.Movement.Fly.Enabled then
        local MoveDirection = Vector3.zero
        
        if UserInputService:IsKeyDown(Enum.KeyCode.W) then MoveDirection = MoveDirection + Camera.CFrame.LookVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.S) then MoveDirection = MoveDirection - Camera.CFrame.LookVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.A) then MoveDirection = MoveDirection - Camera.CFrame.RightVector end
        if UserInputService:IsKeyDown(Enum.KeyCode.D) then MoveDirection = MoveDirection + Camera.CFrame.RightVector end
        
        if MoveDirection.Magnitude > 0 then
            MoveDirection = MoveDirection.Unit * UI.Misc.Movement.Fly.Speed
        end
        
        RootPart.Velocity = MoveDirection
    end

    if Script.Toggles.CFrame and UI.Misc.Movement.CFrame.Enabled then
        RootPart.CFrame = RootPart.CFrame + Humanoid.MoveDirection * UI.Misc.Movement.CFrame.Speed
    end

    if UI.Misc.Client.FaceBackwards then
        Humanoid.AutoRotate = false
        

        local LookDirection = Vector3.new(Camera.CFrame.LookVector.X, 0, Camera.CFrame.LookVector.Z).Unit
        RootPart.CFrame = CFrame.lookAt(RootPart.Position, RootPart.Position - LookDirection)
    else
        Humanoid.AutoRotate = true
    end

    if UI.Misc.Client.AntiStomp then
        if Script.Client.Humanoid.Health <= 5 then
            Script.Functions.ForceReset()
        end
    end
end)

---------------------------------------[[ Hooks ]]---------------------------------------
Script.Hooks.Index = hookmetamethod(game, '__index', LPH_NO_VIRTUALIZE(function(self, Index)
    if not checkcaller() and self == Mouse and Index == "Hit" then
        if UI.Combat.SilentAim.Enabled and Script.Targeting.Target and Script.Targeting.Target.Character then
            return Script.Functions.GetShootingPosition(Script.Targeting.Target.Character)
        end
    end

    return Script.Hooks.Index(self, Index)
end))

Script.Hooks.ServerDesyncHook = hookmetamethod(game, "__index", LPH_NO_VIRTUALIZE(function(self, Index)
    if not checkcaller() and Script.Toggles.ServerDesync and UI.AntiAim.ServerDesync.Enabled and Script.Data.Desync[1] and Script.Client.RootPart and Index == "CFrame" and self == Script.Client.RootPart then
        local CallingScript = tostring(getcallingscript())
        if CallingScript == "CameraModule" then 
            return Script.Data.Desync[1]
        end
    end
    return Script.Hooks.ServerDesyncHook(self, Index)
end))

Script.Hooks.Namecall = hookmetamethod(game, "__namecall", function(Object, ...)
    if not UI.Combat.SilentAim.ForceHit then
        return Script.Hooks.Namecall(Object, ...)
    end

    local Arguments = {...}
    local NameCallMethod = getnamecallmethod()

    if not Script.Functions.TargetExists() then
        return Script.Hooks.Namecall(Object, ...)
    end

    if NameCallMethod == "InvokeServer" and Object.Name == "MainFunction" and #Arguments > 0 and Arguments[1] == "GunCheck" then
        return nil
    end

    if NameCallMethod == "FireServer" and Object.Name == "MainRemote" and #Arguments > 0 and Arguments[1] == "Shoot" then
        if Script.Targeting.Target.Character['Head'] and Arguments[2] and #Arguments[2] > 0 then
            for _, Table in pairs(Arguments[2][1]) do
                Table["Instance"] = Script.Targeting.Target.Character['Head']
            end
            for _, Table in pairs(Arguments[2][2]) do
                Table["thePart"] = Script.Targeting.Target.Character['Head']
                Table["theOffset"] = CFrame.new()
            end
            return Script.Hooks.Namecall(Object, unpack(Arguments))
        end
    end

    return Script.Hooks.Namecall(Object, ...)
end)

Script.Hooks.NewIndex = hookmetamethod(game, "__newindex", LPH_NO_VIRTUALIZE(function(self, Index, Value)
    if tostring(self) == "Humanoid" then
        if UI.Misc.Client.AntiJumpCooldown and Index == "JumpPower" then
            if Value < 50 then
                return
            end
        end

        if UI.Misc.Client.AntiSlow and Index == "WalkSpeed" then
            if Value < 16 then
                return
            end
        end
    end
    return Script.Hooks.NewIndex(self, Index, Value)
end))

---------------------------------------[[ Library ]]---------------------------------------
local TitleString = 'matcha.lol | https://discord.gg/Vsnz2wfjP5 | %A, %B '
local Day = os.date('%d', os.time())
local SecondString = ', %Y.'

local DayString = tostring(Day)
local Suffix = ''

if #DayString == 2 then
    local LastDigit = string.sub(DayString, 2, 2)
    Suffix = LastDigit == '1' and 'st' or LastDigit == '2' and 'nd' or LastDigit == '3' and 'rd' or 'th'
end
TitleString = os.date(TitleString, os.time()) .. Day .. Suffix .. os.date(SecondString, os.time())

do -- [[ UI ]]
    local Window = Library:Window({Name = TitleString, PageAmmount = 7, Size = UDim2.new(0, 500, 0, 600)})
	local Watermark = Library:Watermark(TitleString)
	local KeybindList = Library:KeybindList()

    local CombatTab = Window:Page({Name = 'Combat', Columns = 2})
    local AntiAimTab = Window:Page({Name = 'Anti Aim', Columns = 2})
    local MiscTab = Window:Page({Name = 'Misc', Columns = 2})
    local VisualsTab = Window:Page({Name = 'Visuals', Columns = 2})
    local SettingsTab = Window:Page({Name = 'Settings', Columns = 2})

	do --[[ Combat ]]--
        local TargetingSection = CombatTab:Section({Name = 'Targeting', Side = 1})
        local LegitbotSection = CombatTab:Section({Name = 'Legitbot', Side = 1})
        local SilentAimSection = CombatTab:Section({Name = 'Silent Aim', Side = 1})

        local ChecksSection = CombatTab:Section({Name = 'Checks', Side = 2})
        local TargetVisualsSection = CombatTab:Section({Name = 'Target Visuals', Side = 2})
        local FieldOfViewSection = CombatTab:Section({Name = 'Field of View', Side = 2})

        do --[[ Targeting ]]--
            TargetingSection:Toggle({Name = 'Enable', Flag = 'Targeting Enabled', Callback = function(State)
                UI.Combat.Targeting.Enabled = State
            end}):Keybind({Name = 'Target Bind', Default = Enum.KeyCode.C, Flag = "Targeting Keybind", Mode = "Toggle", Callback = function(Key)
                if not UI.Combat.Targeting.Enabled then return end
                Script.Toggles.Targeting = not Script.Toggles.Targeting

                if UI.Combat.Targeting.Sticky then
                    if not Script.Toggles.Targeting then Script.Targeting.Target = nil; Script.Functions.ResetTargetVisuals(); return end
                    Script.Functions.SetTarget(Script.Drawings.Fov.Radius)
                end
            end})

            TargetingSection:Toggle({Name = 'Sticky', Flag = 'Sticky Targeting', Callback = function(State)
                UI.Combat.Targeting.Sticky = State
            end})

            TargetingSection:Dropdown({Name = 'Hitpoints', Flag = "Hitpoints", Multi = true, Items = {"Head", "UpperTorso", "HumanoidRootPart", "LowerTorso", "LeftUpperArm", "LeftLowerArm", "LeftHand", "RightUpperArm", "RightLowerArm", "RightHand", "LeftUpperLeg", "LeftLowerLeg", "LeftFoot", "RightUpperLeg", "RightLowerLeg", "RightFoot"}, Callback = function(Options)
                UI.Combat.Targeting.Hitpoints = Options
            end})
        end

        do --[[ Legitbot ]]--
            LegitbotSection:Toggle({Name = 'Enable', Flag = 'Legitbot Enabled', Callback = function(State)
                UI.Combat.Legitbot.Enabled = State
            end})

            LegitbotSection:Divider()

            LegitbotSection:Toggle({Name = 'Prediction', Flag = 'Legitbot Prediction Enabled', Callback = function(State)
                UI.Combat.Legitbot.PredictionEnabled = State
            end})

            LegitbotSection:Slider({Name = "Prediction", Min = 0, Max = 1, Suffix = "", Decimals = 0.0001, Flag = "Legitbot Prediction", Default = 0.095, Callback = function(Value)
                UI.Combat.Legitbot.PredictionValue = Value
            end})

            LegitbotSection:Divider()

            LegitbotSection:Slider({Name = "Smoothness", Min = 0, Max = 1, Suffix = "", Decimals = 0.01, Flag = "Legitbot Smoothness", Default = 2, Callback = function(Value)
                UI.Combat.Legitbot.Smoothness = Value
            end})
			LegitbotSection:Toggle({Name = 'Jump Offset', Flag = 'Legitbot Jump Offset Enabled', Callback = function(State)
			    UI.Combat.Legitbot.JumpOffsetEnabled = State
			end})
		
		    LegitbotSection:Slider({Name = "Jump Offset Amount", Min = 0, Max = 10, Suffix = " studs", Decimals = 0.1, Flag = "Legitbot Jump Offset Value", Default = 2.5, Callback = function(Value)
		        UI.Combat.Legitbot.JumpOffsetValue = Value
		    end})

        end

        do --[[ Silent Aim ]]--
            SilentAimSection:Toggle({Name = 'Enable', Flag = 'Silent Aim Enabled', Callback = function(State)
                UI.Combat.SilentAim.Enabled = State
            end})

            SilentAimSection:Toggle({Name = 'Force Hit', Flag = 'Force Hit', Callback = function(State)
                UI.Combat.SilentAim.ForceHit = State
            end})
            
            SilentAimSection:Divider()

            SilentAimSection:Toggle({Name = 'Double Tap', Flag = 'Double Tap', Callback = function(State)
                UI.Combat.SilentAim.DoubleTap = State
            end})

            SilentAimSection:Dropdown({Name = 'Mode', Flag = "Double Tap Mode", Items = {"Activate", "Secret"}, Callback = function(Option)
                UI.Combat.SilentAim.DoubleTapMode = Option
            end})

            SilentAimSection:Divider()

            SilentAimSection:Toggle({Name = 'Prefire Forcefield', Flag = 'Prefire Forcefield', Callback = function(State)
                UI.Combat.SilentAim.Prefire = State
            end})

            SilentAimSection:Slider({Name = "Seconds", Min = 1, Max = 3, Suffix = "s", Decimals = 0.01, Flag = "Prefire Seconds", Default = 3, Callback = function(Value)
                UI.Combat.SilentAim.PrefireSeconds = Value
            end})
        end

        do --[[ Checks ]]--
            ChecksSection:Toggle({Name = 'Knocked', Flag = 'Knocked Check', Callback = function(State)
                UI.Combat.Checks.Knocked = State
            end})

            ChecksSection:Toggle({Name = 'Raycast', Flag = 'Raycast Check', Callback = function(State)
                UI.Combat.Checks.Raycast = State
            end})

            ChecksSection:Toggle({Name = 'Friend', Flag = 'Friend Check', Callback = function(State)
                UI.Combat.Checks.Friend = State
            end})

            ChecksSection:Toggle({Name = 'Forcefield', Flag = 'Forcefield Check', Callback = function(State)
                UI.Combat.Checks.Knocked.Forcefield = State
            end})
        end

        do --[[ Target Visuals ]]--
            TargetVisualsSection:Toggle({Name = 'Highlight', Flag = 'Highlight Target', Callback = function(State)
                UI.Combat.TargetVisuals.Highlight = State
            end})
            
            TargetVisualsSection:Label({Name = "Fill Color"}):Colorpicker({Name = "Fill Color", Flag = "Highlight Fill Color", Default = Library.Theme.Accent, Callback = function(Color)
                TargetHighlight.FillColor = Color
            end})

            TargetVisualsSection:Label({Name = "Outline Color"}):Colorpicker({Name = "Outline Color", Flag = "Highlight Outline Color", Default = Library.Theme.Accent, Callback = function(Color)
                TargetHighlight.OutlineColor = Color
            end})

            TargetVisualsSection:Slider({Name = "Fill Transparency", Min = 0, Max = 1, Suffix = "", Decimals = 0.1, Flag = "Highlight Transparency", Default = 0.5, Callback = function(Value)
                TargetHighlight.FillTransparency = Value
            end})

            TargetVisualsSection:Toggle({Name = 'Name', Flag = 'Target Name', Callback = function(State)
                UI.Combat.TargetVisuals.TargetText = State
            end})

            TargetVisualsSection:Label({Name = "Text Color"}):Colorpicker({Name = "Text Color", Flag = "Text Color", Default = Color3.fromRGB(255, 255, 255), Callback = function(Color)
                Script.Drawings.TargetName.Color = Color
            end})
        end

        do --[[ Field of View ]]--
            FieldOfViewSection:Toggle({Name = 'Visible', Flag = 'Fov Visible', Callback = function(State)
                Script.Drawings.Fov.Visible = State
            end}):Colorpicker({Name = "Fov Color", Flag = "Fov Color", Default = Library.Theme.Accent, Callback = function(Color)
                Script.Drawings.Fov.Color = Color
            end})

            FieldOfViewSection:Toggle({Name = 'Filled', Flag = 'Fov Filled', Callback = function(State)
                Script.Drawings.FilledFov.Visible = State
            end}):Colorpicker({Name = "Filled Color", Flag = "Filled Fov Color", Default = Library.Theme.Accent, Callback = function(Color)
                Script.Drawings.FilledFov.Color = Color
            end})

            FieldOfViewSection:Divider()

            FieldOfViewSection:Slider({Name = "Radius", Min = 0, Max = 1000, Decimals = 1, Suffix = "°", Flag = "Fov Radius", Default = 120, Callback = function(Value)
                Script.Drawings.Fov.Radius = Value
                Script.Drawings.FilledFov.Radius = Value
            end})

            FieldOfViewSection:Slider({Name = "Filled Transparency", Min = 0, Max = 1, Decimals = 0.1, Suffix = "", Flag = "Filled Fov Transparency", Default = 0.2, Callback = function(Value)
                Script.Drawings.FilledFov.Transparency = Value
            end})

            FieldOfViewSection:Slider({Name = "Thickness", Min = 0, Max = 10, Decimals = 0.1, Suffix = "", Flag = "Fov Thickness", Default = 1, Callback = function(Value)
                Script.Drawings.Fov.Thickness = Value
            end})

            FieldOfViewSection:Divider()

            FieldOfViewSection:Toggle({Name = 'Stick Target', Flag = 'Stick Fov Target', Callback = function(State)
                UI.Combat.Fov.StickTarget = State
            end})

            FieldOfViewSection:Toggle({Name = 'Stick Barrel', Flag = 'Stick Fov Barrel', Callback = function(State)
                UI.Combat.Fov.StickBarrel = State
            end})
        end
    end 

    do --[[ Anti Aim ]]--
        local ServerDesyncSection = AntiAimTab:Section({Name = 'Desync', Side = 1})
        local VelocitySection = AntiAimTab:Section({Name = 'Velocity', Side = 2})

        do --[[ Desync ]]--
            ServerDesyncSection:Toggle({Name = 'Server Desync', Flag = 'Server Desync', Callback = function(State)
                UI.AntiAim.ServerDesync.Enabled = State
            end}):Keybind({Name = 'Server Desync Bind', Default = Enum.KeyCode.G, Flag = "Server Desync Keybind", Mode = "Toggle", Callback = function(Key)
                if not UI.AntiAim.ServerDesync.Enabled then return end
                Script.Toggles.ServerDesync = not Script.Toggles.ServerDesync
                Script.Drawings.DesyncStatus.Text = "Server Desync: "..tostring(Script.Toggles.ServerDesync and UI.AntiAim.ServerDesync.Enabled)
            end})

            ServerDesyncSection:Toggle({Name = 'Desync Status', Flag = 'Desync Status', Callback = function(State)
                Script.Drawings.DesyncStatus.Visible = State
            end}):Colorpicker({Name = "Status Color", Flag = "Status Color", Default = Color3.fromRGB(255, 255, 255), Callback = function(Color)
                Script.Drawings.DesyncStatus.Color = Color
            end})

            ServerDesyncSection:Label({Name = "Keybind Shoot"}):Keybind({Name = 'Keybind Shoot', Default = Enum.KeyCode.H, Flag = "Keybind Shoot Keybind", Mode = "Toggle", Callback = function(Key)
                if UI.AntiAim.ServerDesync.Mode ~= "Keybind Shoot" then return end

                Script.Functions.KeybindShoot()
            end})

            ServerDesyncSection:Dropdown({Name = 'Mode', Flag = "Server Desync Mode", Items = {"Custom", "Safe Shoot", "Keybind Shoot", "Underground", "Spin", "Mole", "Moke", "Mok", "Musk", "Tool"}, Callback = function(Option)
                UI.AntiAim.ServerDesync.Mode = Option
            end})

            ServerDesyncSection:Divider()

            ServerDesyncSection:Slider({Name = "Custom X Position", Min = -30, Max = 30, Suffix = "", Decimals = 1, Flag = "Custom X Position", Default = 0, Callback = function(Value)
                UI.AntiAim.ServerDesync.Custom.X = Value
            end})

            ServerDesyncSection:Slider({Name = "Custom Y Position", Min = -30, Max = 30, Suffix = "", Decimals = 1, Flag = "Custom Y Position", Default = 0, Callback = function(Value)
                UI.AntiAim.ServerDesync.Custom.Y = Value
            end})

            ServerDesyncSection:Slider({Name = "Custom Z Position", Min = -30, Max = 30, Suffix = "", Decimals = 1, Flag = "Custom Z Position", Default = 0, Callback = function(Value)
                UI.AntiAim.ServerDesync.Custom.Z = Value
            end})

            ServerDesyncSection:Divider()

            ServerDesyncSection:Slider({Name = "Custom X Angle", Min = -30, Max = 30, Suffix = "", Decimals = 1, Flag = "Custom X Angle", Default = 0, Callback = function(Value)
                UI.AntiAim.ServerDesync.Custom.XX = Value
            end})

            ServerDesyncSection:Slider({Name = "Custom Y Angle", Min = -30, Max = 30, Suffix = "", Decimals = 1, Flag = "Custom Y Angle", Default = 0, Callback = function(Value)
                UI.AntiAim.ServerDesync.Custom.YY = Value
            end})

            ServerDesyncSection:Slider({Name = "Custom Z Angle", Min = -30, Max = 30, Suffix = "", Decimals = 1, Flag = "Custom Z Angle", Default = 0, Callback = function(Value)
                UI.AntiAim.ServerDesync.Custom.ZZ = Value
            end})
        end

        do --[[ Velocity ]]--
            VelocitySection:Toggle({Name = 'Velocity Spoofer', Flag = 'Velocity Spoofer', Callback = function(State)
                UI.AntiAim.VelocitySpoofer.Enabled = State
            end}):Keybind({Name = 'Velocity Spoofer Bind', Default = Enum.KeyCode.B, Flag = "Velocity Spoofer Keybind", Mode = "Toggle", Callback = function(Key)
                if not UI.AntiAim.VelocitySpoofer.Enabled then return end
                Script.Toggles.VelocitySpoofer = not Script.Toggles.VelocitySpoofer
                Script.Drawings.VelocityStatus.Text = "Velocity Spoofer: "..tostring(Script.Toggles.VelocitySpoofer and UI.AntiAim.VelocitySpoofer.Enabled)
            end})

            VelocitySection:Toggle({Name = 'Desync Status', Flag = 'Desync Status', Callback = function(State)
                Script.Drawings.VelocityStatus.Visible = State
            end}):Colorpicker({Name = "Status Color", Flag = "Status Color", Default = Color3.fromRGB(255, 255, 255), Callback = function(Color)
                Script.Drawings.VelocityStatus.Color = Color
            end})

            VelocitySection:Dropdown({Name = 'Mode', Flag = "Velocity Spoofer Mode", Items = {"Random", "Custom"}, Callback = function(Option)
                UI.AntiAim.VelocitySpoofer.Mode = Option
            end})

            VelocitySection:Divider()

            VelocitySection:Slider({Name = "Custom X Velocity", Min = -1000, Max = 1000, Suffix = "", Decimals = 1, Flag = "Custom X Velocity", Default = 0, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.X = Value
            end})

            VelocitySection:Slider({Name = "Custom Y Velocity", Min = -1000, Max = 1000, Suffix = "", Decimals = 1, Flag = "Custom Y Velocity", Default = 0, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.Y = Value
            end})

            VelocitySection:Slider({Name = "Custom Z Velocity", Min = -1000, Max = 1000, Suffix = "", Decimals = 1, Flag = "Custom Z Velocity", Default = 0, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.Z = Value
            end})

            VelocitySection:Divider()

            VelocitySection:Slider({Name = "Random X Minimum", Min = -10000, Max = 1, Suffix = "", Decimals = 1, Flag = "Velocity X Minimum", Default = 1, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.MinX = Value
            end})

            VelocitySection:Slider({Name = "Random X Maximum", Min = 1, Max = 10000, Suffix = "", Decimals = 1, Flag = "Velocity X Maximum", Default = 1, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.MaxX = Value
            end})

            VelocitySection:Slider({Name = "Random Y Minimum", Min = -10000, Max = 1, Suffix = "", Decimals = 1, Flag = "Velocity Y Minimum", Default = 1, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.MinY = Value
            end})

            VelocitySection:Slider({Name = "Random Y Maximum", Min = 1, Max = 10000, Suffix = "", Decimals = 1, Flag = "Velocity Y Maximum", Default = 1, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.MaxY = Value
            end})

            VelocitySection:Slider({Name = "Random Z Minimum", Min = -10000, Max = 1, Suffix = "", Decimals = 1, Flag = "Velocity Z Minimum", Default = 1, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.MinZ = Value
            end})

            VelocitySection:Slider({Name = "Random Z Maximum", Min = 1, Max = 10000, Suffix = "", Decimals = 1, Flag = "Velocity Z Maximum", Default = 1, Callback = function(Value)
                UI.AntiAim.VelocitySpoofer.Custom.MaxZ = Value
            end})


            VelocitySection:Divider()
        end
    end

    do --[[ Misc ]]--
        local Movement = MiscTab:Section({Name = 'Movement', Side = 1})
        local AvatarLoader = MiscTab:Section({Name = 'Avatar', Side = 1})
        local ClientStuff = MiscTab:Section({Name = 'Client', Side = 2})

        do -- movement
            Movement:Toggle({Name = 'Fly', Flag = 'Fly', Callback = function(State)
                UI.Misc.Movement.Fly.Enabled = State
            end}):Keybind({Name = 'Fly Bind', Default = Enum.KeyCode.X, Flag = "Fly Keybind", Mode = "Toggle", Callback = function(Key)
                if not UI.Misc.Movement.Fly.Enabled then return end
                Script.Toggles.Fly = not Script.Toggles.Fly
            end})

            Movement:Slider({Name = "Fly Speed", Min = 10, Max = 250, Suffix = "", Decimals = 1, Flag = "Fly Speed", Default = 50, Callback = function(Value)
                UI.Misc.Movement.Fly.Speed = Value
            end})

            Movement:Divider()

            Movement:Toggle({Name = 'CFrame Speed', Flag = 'CFrame', Callback = function(State)
                UI.Misc.Movement.CFrame.Enabled = State
            end}):Keybind({Name = 'CFrame Speed Bind', Default = Enum.KeyCode.X, Flag = "CFrame Keybind", Mode = "Toggle", Callback = function(Key)
                if not UI.Misc.Movement.CFrame.Enabled then return end
                Script.Toggles.CFrame = not Script.Toggles.CFrame
            end})

            Movement:Slider({Name = "Speed", Min = 0, Max = 5, Suffix = "", Decimals = 0.1, Flag = "CFrame Speed", Default = 1, Callback = function(Value)
                UI.Misc.Movement.CFrame.Speed = Value
            end})

            Movement:Divider()

            Movement:Toggle({Name = 'Infinite Jump', Flag = 'Infinite Jump', Callback = function(State)
                if State then
                    Script.Connections["Infinite Jumps Connection"] = UserInputService.JumpRequest:Connect(function()
                        if not Script.Functions.ClientChecks() then return end

                        if not Script.Debounces['Infinite Jump Debounce'] then
                            Script.Debounces['Infinite Jump Debounce'] = true
                            Script.Client.Humanoid:ChangeState(Enum.HumanoidStateType.Jumping)
                            task.wait()
                            Script.Debounces['Infinite Jump Debounce'] = false
                        end
                    end)
                else
                    if Script.Connections["Infinite Jumps Connection"] then
                        Script.Connections["Infinite Jumps Connection"]:Disconnect()
                        Script.Connections["Infinite Jumps Connection"] = nil
                        Script.Debounces['Infinite Jump Debounce'] = false
                    end 
                end
            end})
        end

        do -- client stuff
            ClientStuff:Toggle({Name = 'No Jump Cooldown', Flag = 'No Jump Cooldown', Callback = function(State)
                UI.Misc.Client.AntiJumpCooldown = State
            end})

            ClientStuff:Toggle({Name = 'No Walkspeed Restriction', Flag = 'No Walkspeed Restriction', Callback = function(State)
                UI.Misc.Client.AntiSlow = State
            end})

            ClientStuff:Toggle({Name = 'Anti Stomp', Flag = 'Anti Stomp', Callback = function(State)
                UI.Misc.Client.AntiStomp = State
            end})

            ClientStuff:Toggle({Name = 'Noclip', Flag = 'Noclip', Callback = function(State)
                -- Tạo connection mới khi toggle
                if State then
                    Script.Connections["NoclipConnection"] = Script.Functions.CreateConnection(RunService.Stepped, function()
                        if Library.Flags['Noclip'] and Script.Functions.ClientChecks() then
                            for _, v in pairs(Script.Client.Character:GetDescendants()) do
                                if v:IsA("BasePart") and v.CanCollide then
                                    v.CanCollide = false
                                end
                            end
                        end
                    end)
                    Library:Notification("Noclip ✅", 2, Library.Theme.Accent)
                else
                    -- Cleanup connection khi tắt
                    if Script.Connections["NoclipConnection"] then
                        Script.Connections["NoclipConnection"]:Disconnect()
                        Script.Connections["NoclipConnection"] = nil
                    end
                    Library:Notification("Noclip ❌", 2, Color3.fromRGB(255, 0, 0))
                end
            end}):Keybind({Name = '', Default = Enum.KeyCode.T, Flag = "Noclip Keybind", Mode = "Toggle", Callback = function(Key)
                -- Keybind tự động flip toggle
                Library.Flags['Noclip'] = not Library.Flags['Noclip']
            end})
            ClientStuff:Toggle({Name = 'Rapid Fire', Flag = 'Rapid Fire', Callback = function(State)
                getgenv().RapidFireEnabled = State
                if not State then
                    getgenv().is_firing = false
                    -- Reset cooldown khi tắt
                    for func, orig in pairs(originalCooldowns) do
                        for i = 1, debug.getinfo(func).nups do
                            local val = debug.getupvalue(func, i)
                            if val == 0.00000000000000000001 then
                                debug.setupvalue(func, i, orig)
                                break
                            end
                        end
                    end
                    originalCooldowns = {}
                end
            end})
            ClientStuff:Divider()

            ClientStuff:Toggle({Name = 'Animation', Flag = 'Animation Enabled', Callback = function(State)
                if State then
                    Script.Functions.LoadAnimation(Script.Animation.Animations[UI.Misc.Client.Animation.Selected])

                    task.wait(0.5)
                    if Script.Animation.Animation then
                        Script.Animation.Animation:AdjustSpeed(UI.Misc.Client.Animation.Speed)
                    end
                else
                    Script.Animation.Animation:Stop()
                    Script.Animation.AnimationObject:Destroy()

                    Script.Animation.Animation = nil
                    Script.Animation.AnimationObject = nil
                end
            end})

            ClientStuff:Dropdown({Name = "Animation", Flag = "Animation", Default = "Floss", Items = {"Floss", "Flex Walk", "HUGO Let's Drive!"}, Callback = function(Option)
                UI.Misc.Client.Animation.Selected = Option
            end})

            ClientStuff:Slider({Name = "Animation Speed", Min = 0, Max = 50, Suffix = "", Decimals = 0.1, Flag = "Animation Speed", Default = 1, Callback = function(Value)
                UI.Misc.Client.Animation.Speed = Value
                if Script.Animation.Animation then
                    Script.Animation.Animation:AdjustSpeed(UI.Misc.Client.Animation.Speed)
                end
            end})
        end

        do -- avatar loader
            local AvatarListbox = AvatarLoader:Listbox({Flag = "Avatar Name", Options = matcha.Characters, Callback = function(Option)
				UI.Misc.Client.AvatarChanger.Name = Option
			end}) 
            AvatarLoader:Button({Name = "Load Character", Callback = function() Script.Functions.LoadAvatar(AvatarListbox:Get()) end})
            AvatarLoader:Button({Name = "Refresh List", Callback = function()
				if isfolder("matcha/Characters") then
					for I, V in pairs(listfiles("matcha/Characters")) do
						local FileName = V:match("^.+[\\/](.+)$")
						local NameWithoutExtension = FileName:match("(.+)%..+$")
						local Found = false
						for J, ExistingConfig in pairs(matcha.Characters) do
							if ExistingConfig == NameWithoutExtension then
								Found = true
								break
							end
						end
						if not Found then
							table.insert(matcha.Characters, NameWithoutExtension)
						end
					end
				else
					makefolder("matcha/Characters")
				end
				AvatarListbox:Refresh(matcha.Characters)
			end})
            AvatarLoader:Toggle({Name = 'Load After Death', Flag = 'Load Avatar After Death', Callback = function(State)
                UI.Misc.Client.AvatarChanger.LoadOnDeath = State
            end})
        end
    end
	do --[[ Bullet Tracers (HEADSHOTS.CC STYLE - BEAM + PARTS + DROPDOWN) ]]--
	    local BulletTracerSection = VisualsTab:Section({Name = 'Bullet Tracers', Side = 1})
	
	    BulletTracerSection:Toggle({Name = 'Enabled', Flag = 'BulletTracer Enabled', Default = false, Callback = function(State)
	        UI.Visuals.BulletTracer.Enabled = State
	        if not State then
	            -- Cleanup all tracers khi tắt
	            for _, tracerData in pairs(Script.ActiveTracers or {}) do
	                if tracerData.startPart then tracerData.startPart:Destroy() end
	                if tracerData.endPart then tracerData.endPart:Destroy() end
	                if tracerData.beam then tracerData.beam:Destroy() end
	            end
	            Script.ActiveTracers = {}
	        end
	    end}):Colorpicker({Name = "Color", Flag = "BulletTracer Color", Default = Color3.fromRGB(155, 125, 175), Callback = function(Color)
	        UI.Visuals.BulletTracer.Color = Color
	    end})
	
	    local Textures = {
	        "rbxassetid://12781852245",  -- Pink Glow (Default)
	        "rbxassetid://241650934",    -- Classic White
	        "rbxassetid://4996891970",   -- Neon Blue
	        "rbxassetid://7151778303",   -- Red Laser
	        "rbxassetid://6504428863",   -- Sparkle
	        ""                          -- None (transparent)
	    }
	
	    BulletTracerSection:Dropdown({Name = 'Texture', Flag = 'BulletTracer Texture', Items = Textures, Default = "rbxassetid://12781852245", Callback = function(Option)
	        UI.Visuals.BulletTracer.SelectedTexture = Option
	        UI.Visuals.BulletTracer.TextureID = Option
	    end})
	
	
	    BulletTracerSection:Slider({Name = "Size", Min = 0, Max = 2, Decimals = 0.1, Suffix = "", Flag = "BulletTracer Size", Default = 0.4, Callback = function(Value)
	        UI.Visuals.BulletTracer.Size = Value
	    end})
	
	    BulletTracerSection:Slider({Name = "Transparency", Min = 0, Max = 1, Decimals = 0.1, Suffix = "", Flag = "BulletTracer Transparency", Default = 0, Callback = function(Value)
	        UI.Visuals.BulletTracer.Transparency = Value
	    end})
	
	    BulletTracerSection:Slider({Name = "Time Alive", Min = 1, Max = 10, Suffix = "s", Flag = "BulletTracer Time", Default = 3, Callback = function(Value)
	        UI.Visuals.BulletTracer.TimeAlive = Value
	    end})
	end
	do -- Settings Tab
		local SettingsSection = SettingsTab:Section({Name = "Settings", Side = 2})
		local ConfigsSection = SettingsTab:Section({Name = "Profiles", Side = 1})

		for Index, Value in Library.Theme do 
			SettingsSection:Label({Name = Index, Alignment = "Left"}):Colorpicker({ Name = Index, Default = Value, Flag = "Theme"..Index, Callback = function(Color) 
				Library.Theme[Index] = Color
				Library:ChangeTheme(Index, Color)
			end})
		end

		SettingsSection:Label({Name = "Menu Keybind", Alignment = "Left"}):Keybind({Name = "Menu Keybind", Flag = "Menu Keybind", Default = Enum.KeyCode.RightControl, Mode = "Toggle", Callback = function(Value)
			Library.MenuKeybind = Library.Flags["Menu Keybind"].Key
		end})

		SettingsSection:Toggle({Name = "Watermark", Flag = "Watermark", Default = false, Callback = function(Value)
			Watermark:SetVisibility(Value)
		end})

		SettingsSection:Toggle({Name = "Keybind List", Flag = "Keybind List", Default = false, Callback = function(Value)
			KeybindList:SetVisibility(Value)
		end})

		SettingsSection:Dropdown({Name = "Tweening Style", Flag = "Tweening Style", Default = "Exponential", Items = {"Linear", "Sine", "Quad", "Cubic", "Quart", "Quint", "Exponential", "Circular", "Back", "Elastic", "Bounce"}, Callback = function(Value)
			Library.Tween.Style = Enum.EasingStyle[Value]
		end})

		SettingsSection:Dropdown({Name = "Tweening Direction", Flag = "Tweening Direction", Default = "Out", Items = {"In", "Out", "InOut"}, Callback = function(Value)
			Library.Tween.Direction = Enum.EasingDirection[Value]
		end})

		SettingsSection:Slider({Name = "Tweening Time", Min = 0, Max = 5, Default = 0.25, Decimals = 0.01, Flag = "Tweening Time", Callback = function(Value)
			Library.Tween.Time = Value
		end})

		SettingsSection:Button({Name = "Rejoin Server", Callback = function()
		    Library:Notification("Rejoining current server...", 3, Library.Theme.Accent)
		    local ts = game:GetService("TeleportService")
		    ts:TeleportToPlaceInstance(game.PlaceId, game.JobId, LocalPlayer)
		end})
		
		-- SERVERHOP (tự động tìm server khác có slot trống)
		SettingsSection:Button({Name = "Serverhop", Callback = function()
		    Library:Notification("Serverhopping...", 3, Library.Theme.Accent)
		    task.spawn(function()
		        local Http = game:GetService("HttpService")
		        local TS = game:GetService("TeleportService")
		        local req = Http:JSONDecode(game:HttpGet("https://games.roblox.com/v1/games/"..game.PlaceId.."/servers/Public?sortOrder=Asc&limit=100"))
		        
		        local servers = {}
		        for i,v in pairs(req.data) do
		            if v.playing < v.maxPlayers and v.id ~= game.JobId then
		                table.insert(servers, v.id)
		            end
		        end
		        
		        if #servers > 0 then
		            TS:TeleportToPlaceInstance(game.PlaceId, servers[math.random(1, #servers)], LocalPlayer)
		        else
		            Library:Notification("No available servers found!", 4, Color3.fromRGB(255,0,0))
		        end
		    end)
		end})
		SettingsSection:Button({Name = "Unload library", Callback = function()
			Library:Unload()
		end})

		local ConfigName 
		local ConfigSelected

		local ConfigsListbox = ConfigsSection:Listbox({Items = { }, Name = "Configs", Flag = "Configs List", Callback = function(Value)
			ConfigSelected = Value
		end})

		ConfigsSection:Textbox({Name = "Config Name", Placeholder = ". .", Flag = "Config Name", Callback = function(Value)
			ConfigName = Value
		end})

		ConfigsSection:Button({Name = "Create Config", Callback = function()
			if not isfile(Library.Folders.Configs .. "/" .. ConfigName .. ".json") then
				writefile(Library.Folders.Configs .. "/" .. ConfigName .. ".json", Library:GetConfig())

				Library:RefreshConfigsList(ConfigsListbox)
			else
				Library:Notification("Config '" .. ConfigName .. ".json' already exists", 3, Color3.FromR(255, 0, 0))
				return
			end
		end})

		ConfigsSection:Button({Name = "Load Config", Callback = function()
			if ConfigSelected then
				Library:LoadConfig(readfile(Library.Folders.Configs .. "/" .. ConfigSelected))
			end

			Library:Thread(function()
				task.wait(0.1)

				for Index, Value in Library.Theme do 
					Library.Theme[Index] = Library.Flags["Theme"..Index].Color
					Library:ChangeTheme(Index, Library.Flags["Theme"..Index].Color)
				end    
			end)
		end})

		ConfigsSection:Button({Name = "Delete Config", Callback = function()
			if ConfigSelected then
				Library:DeleteConfig(ConfigSelected)

				Library:RefreshConfigsList(ConfigsListbox)
			end
		end})

		ConfigsSection:Button({Name = "Save Config", Callback = function()
			if ConfigSelected then
				Library:SaveConfig(ConfigSelected)
			end
		end})

		ConfigsSection:Button({Name = "Refresh Configs", Callback = function()
			Library:RefreshConfigsList(ConfigsListbox)
		end})

		Library:RefreshConfigsList(ConfigsListbox)
	end
end


utility.get_gun = function()
    local char = LocalPlayer.Character
    if not char then return nil end
    for _, tool in ipairs(char:GetChildren()) do
        if tool:IsA("Tool") and tool:FindFirstChild("Ammo") then
            return tool
        end
    end
    return nil
end

utility.rapid = function(tool)
    if tool and tool.Parent then
        pcall(function() tool:Activate() end)
    end
end

UserInputService.InputBegan:Connect(function(input)
    if (input.UserInputType == Enum.UserInputType.MouseButton1 
        or input.UserInputType == Enum.UserInputType.Touch)
        and getgenv().RapidFireEnabled 
    then
        local gun = utility.get_gun()
        if gun and not getgenv().is_firing then
            getgenv().is_firing = true
            task.spawn(function()
                while getgenv().is_firing and getgenv().RapidFireEnabled and utility.get_gun() do
                    utility.rapid(utility.get_gun())
                    task.wait(0.1)
                end
            end)
        end
    end
end)

-- Dừng bắn khi thả chuột hoặc thả tay
UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 
        or input.UserInputType == Enum.UserInputType.Touch 
    then
        getgenv().is_firing = false
    end
end)

game:GetService("RunService").Heartbeat:Connect(function()
    local tool = LocalPlayer.Character and LocalPlayer.Character:FindFirstChildOfClass("Tool")
    if getgenv().RapidFireEnabled and tool and tool:FindFirstChild("GunScript") then 
        for _, v in ipairs(getconnections(tool.Activated)) do
            local funcinfo = debug.getinfo(v.Function)
            for i = 1, funcinfo.nups do
                local c = debug.getupvalue(v.Function, i)
                if type(c) == "number" then 
                    debug.setupvalue(v.Function, i, 0)
                end
            end
        end
    end
end)

setfpscap(240)
