local ScreenGui = Instance.new("ScreenGui")
local gemSpawnerFrame = Instance.new("Frame")
local gemNameTextbox = Instance.new("TextBox")
local spawnButton = Instance.new("TextButton")
local gemLabel = Instance.new("TextLabel")
local uiCornerSpawnerFrame = Instance.new("UICorner")
local uiCornerGemNameTextbox = Instance.new("UICorner")
local uiCornerSpawnButton = Instance.new("UICorner")
local uiStrokeSpawnerFrame = Instance.new("UIStroke")

-- Set parent for ScreenGui
ScreenGui.Parent = game:GetService("CoreGui")

-- Gem Spawner UI
gemSpawnerFrame.Name = "GemSpawnerFrame"
gemSpawnerFrame.Parent = ScreenGui
gemSpawnerFrame.BackgroundColor3 = Color3.fromRGB(10, 10, 40)
gemSpawnerFrame.Size = UDim2.new(0, 300, 0, 150)
gemSpawnerFrame.Position = UDim2.new(0.5, -150, 0.5, -75)
gemSpawnerFrame.Active = true
gemSpawnerFrame.Draggable = true -- Makes the UI movable

-- Rounded corners for the UI
uiCornerSpawnerFrame.CornerRadius = UDim.new(0, 10)
uiCornerSpawnerFrame.Parent = gemSpawnerFrame

-- Outline for the UI
uiStrokeSpawnerFrame.Parent = gemSpawnerFrame
uiStrokeSpawnerFrame.Thickness = 2
uiStrokeSpawnerFrame.Color = Color3.fromRGB(70, 130, 180)

-- Gem Spawner Label
gemLabel.Name = "GemLabel"
gemLabel.Parent = gemSpawnerFrame
gemLabel.BackgroundTransparency = 1
gemLabel.Size = UDim2.new(1, 0, 0, 40)
gemLabel.Position = UDim2.new(0, 0, 0, 10)
gemLabel.Text = "Gem Spawner"
gemLabel.TextColor3 = Color3.fromRGB(255, 255, 255)
gemLabel.TextSize = 24
gemLabel.Font = Enum.Font.GothamBold

-- Gem Name Textbox
gemNameTextbox.Name = "GemNameTextbox"
gemNameTextbox.Parent = gemSpawnerFrame
gemNameTextbox.Size = UDim2.new(0, 200, 0, 30)
gemNameTextbox.Position = UDim2.new(0.5, -100, 0.5, -20)
gemNameTextbox.Text = "Enter Gem Amount"
gemNameTextbox.TextColor3 = Color3.fromRGB(255, 255, 255)
gemNameTextbox.Font = Enum.Font.Gotham
gemNameTextbox.TextSize = 18
gemNameTextbox.BackgroundColor3 = Color3.fromRGB(50, 50, 90)

uiCornerGemNameTextbox.CornerRadius = UDim.new(0, 10)
uiCornerGemNameTextbox.Parent = gemNameTextbox

-- Spawn Button
spawnButton.Name = "SpawnButton"
spawnButton.Parent = gemSpawnerFrame
spawnButton.Size = UDim2.new(0, 200, 0, 40) -- Adjusted size to fit within UI
spawnButton.Position = UDim2.new(0.5, -100, 0.5, 20) -- Adjusted position
spawnButton.Text = "Add Gems"
spawnButton.TextColor3 = Color3.fromRGB(255, 255, 255)
spawnButton.Font = Enum.Font.GothamBold
spawnButton.TextSize = 20
spawnButton.BackgroundColor3 = Color3.fromRGB(70, 130, 180) -- Adjusted to match UI color

uiCornerSpawnButton.CornerRadius = UDim.new(0, 10)
uiCornerSpawnButton.Parent = spawnButton

-- Function to update the gem display
local function updateGemDisplay(amount)
    local newGemAmount = tonumber(amount) or 0  -- Ensure it's a number
    game:GetService("Players").LocalPlayer.PlayerGui.Main.Top.Diamonds.Amount.Text = newGemAmount
    game:GetService("Players").LocalPlayer.PlayerGui.Main.Left["Diamonds Desktop"].Amount.Text = newGemAmount
end

-- Button Functionality
spawnButton.MouseButton1Click:Connect(function()
    -- Get the amount from the textbox
    local gemAmount = gemNameTextbox.Text

    -- Update gem display
    updateGemDisplay(gemAmount)

    print("Added gems: " .. gemAmount) -- Confirmation message
end)

-- Initialize gem display on startup
updateGemDisplay(0)  -- Start with 0 gems
