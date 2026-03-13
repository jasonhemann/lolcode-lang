local library = loadstring(game:GetObjects("rbxassetid://7657867786")[1].Source)()
local Wait = library.subs.Wait -- For 'while Wait() do' loops, ensuring GUI remains responsive.

-- Create the main window
local UtilitySuite = library:CreateWindow({
    Name = "Mad.lol",
    Themeable = {
        Info = "Mad.lol"
    }
})

-- Tabs
local MainTab = UtilitySuite:CreateTab({
    Name = "kawaii features"
})
local SettingsTab = UtilitySuite:CreateTab({
    Name = "Settings"
})

-- Main Tab Sections
local CameraLockSection = MainTab:CreateSection({
    Name = "Camera Lock"
})

local SpeedSection = MainTab:CreateSection({
    Name = "Speed",
    Side = "Right" -- Moves this section to the right side of the UI
})

local FlySection = MainTab:CreateSection({
    Name = "Fly"
})

-- Default Configuration
getgenv().ScriptConfig = {
    CameraLockConfig = {
        ToggleKey = Enum.KeyCode.C,
        Prediction = 0.1
    },
    SpeedConfig = {
        ToggleKey = Enum.KeyCode.Z,
        Multiplier = 10
    },
    FlyConfig = {
        ToggleKey = Enum.KeyCode.X,
        Speed = 50,
        VerticalSpeed = 5
    }
}

-- Variables for Toggle States
local cameraLockToggleState = false
local speedToggleState = false
local flyToggleState = false

-- Services
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")
local StarterGui = game:GetService("StarterGui")
local Workspace = game:GetService("Workspace")

-- Local Player Setup
local player = Players.LocalPlayer
local character = player.Character or player.CharacterAdded:Wait()
local HRP = character:WaitForChild("HumanoidRootPart", 10)

-- Notify Function
local function Notify(message)
    StarterGui:SetCore("SendNotification", {
        Title = "Notification",
        Text = message,
        Duration = 1
    })
end

-- Toggle Camera Lock
local function toggleCameraLock()
    cameraLockActive = not cameraLockActive
    if cameraLockActive then
        local closestPlayer = nil
        local closestDistance = math.huge
        local mouse = player:GetMouse()

        for _, targetPlayer in ipairs(Players:GetPlayers()) do
            if targetPlayer ~= player and targetPlayer.Character and targetPlayer.Character:FindFirstChild("HumanoidRootPart") then
                local targetHRP = targetPlayer.Character.HumanoidRootPart
                local screenPosition, onScreen = Workspace.CurrentCamera:WorldToScreenPoint(targetHRP.Position)
                local cursorPosition = Vector2.new(mouse.X, mouse.Y)

                if onScreen then
                    local distance = (cursorPosition - Vector2.new(screenPosition.X, screenPosition.Y)).Magnitude
                    if distance < closestDistance then
                        closestDistance = distance
                        closestPlayer = targetPlayer
                    end
                end
            end
        end

        if closestPlayer then
            local humanoid = closestPlayer.Character.Humanoid
            Notify("Locked onto: " .. closestPlayer.Name .. " | Health: " .. math.floor(humanoid.Health))

            RunService:BindToRenderStep("cameraLock", Enum.RenderPriority.Camera.Value, function()
                if closestPlayer and closestPlayer.Character and closestPlayer.Character:FindFirstChild("HumanoidRootPart") then
                    local targetHRP = closestPlayer.Character.HumanoidRootPart
                    Workspace.CurrentCamera.CFrame = CFrame.lookAt(
                        Workspace.CurrentCamera.CFrame.Position,
                        targetHRP.Position + (targetHRP.Velocity * getgenv().ScriptConfig.CameraLockConfig.Prediction)
                    )
                else
                    toggleCameraLock()
                end
            end)
        else
            Notify("no")
            cameraLockActive = false
        end
    else
        Notify("cam lock off")
        RunService:UnbindFromRenderStep("cameraLock")
    end
end

-- Speed Toggle
local function toggleSpeed()
    speedActive = not speedActive
    if speedActive then
        RunService:BindToRenderStep("cframeSpeed", Enum.RenderPriority.Character.Value, function()
            local moveDirection = Vector3.zero
            local camera = Workspace.CurrentCamera

            if UserInputService:IsKeyDown(Enum.KeyCode.W) then
                moveDirection += (camera.CFrame.LookVector * Vector3.new(1, 0, 1)).Unit
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.S) then
                moveDirection -= (camera.CFrame.LookVector * Vector3.new(1, 0, 1)).Unit
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.A) then
                moveDirection -= (camera.CFrame.RightVector * Vector3.new(1, 0, 1)).Unit
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.D) then
                moveDirection += (camera.CFrame.RightVector * Vector3.new(1, 0, 1)).Unit
            end

            HRP.CFrame = HRP.CFrame + (moveDirection * getgenv().ScriptConfig.SpeedConfig.Multiplier)
        end)
        Notify("Speed Enabled.")
    else
        RunService:UnbindFromRenderStep("cframeSpeed")
        Notify("Speed Disabled.")
    end
end

-- Fly Toggle
local function toggleFly()
    flyActive = not flyActive
    if flyActive then
        local flyLoop
        flyLoop = RunService.RenderStepped:Connect(function()
            if not flyActive then
                flyLoop:Disconnect()
                return
            end

            local direction = Vector3.zero
            if UserInputService:IsKeyDown(Enum.KeyCode.W) then
                direction += Workspace.CurrentCamera.CFrame.LookVector
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.S) then
                direction -= Workspace.CurrentCamera.CFrame.LookVector
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.A) then
                direction -= Workspace.CurrentCamera.CFrame.RightVector
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.D) then
                direction += Workspace.CurrentCamera.CFrame.RightVector
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.Space) then
                direction += Vector3.new(0, getgenv().ScriptConfig.FlyConfig.VerticalSpeed, 0)
            end
            if UserInputService:IsKeyDown(Enum.KeyCode.LeftControl) then
                direction -= Vector3.new(0, getgenv().ScriptConfig.FlyConfig.VerticalSpeed, 0)
            end

            HRP.Velocity = direction.Magnitude > 0 and direction.Unit * getgenv().ScriptConfig.FlyConfig.Speed or Vector3.new(0, 0.1, 0)
        end)
        Notify("Fly Enabled.")
    else
        HRP.Velocity = Vector3.new(0, 0, 0)
        Notify("Fly Disabled.")
    end
end

-- UI Elements Setup
CameraLockSection:AddToggle({
    Name = "Enable Camera Lock (C)",
    Flag = "CameraLockSection_CameraLock",
    Callback = function(state)
        cameraLockToggleState = state
    end
})

CameraLockSection:AddTextBox({
    Name = "Prediction Value",
    Flag = "CameraLockSection_PredictionValue",
    Placeholder = "Enter Prediction",
    Callback = function(value)
        local numValue = tonumber(value)
        if numValue then
            getgenv().ScriptConfig.CameraLockConfig.Prediction = numValue
            Notify("Camera Lock Prediction set to: " .. numValue)
        else
            Notify("Invalid Prediction Value!")
        end
    end
})

SpeedSection:AddToggle({
    Name = "Cframe (Z)",
    Flag = "SpeedSection_Speed",
    Callback = function(state)
        speedToggleState = state
    end
})

SpeedSection:AddSlider({
    Name = "Speed Multiplier",
    Flag = "SpeedSection_SpeedMultiplier",
    Value = getgenv().ScriptConfig.SpeedConfig.Multiplier,
    Min = 1,
    Max = 50,
    Callback = function(value)
        getgenv().ScriptConfig.SpeedConfig.Multiplier = value
    end
})

FlySection:AddToggle({
    Name = "Fly (X)",
    Flag = "FlySection_Fly",
    Callback = function(state)
        flyToggleState = state
    end
})

FlySection:AddSlider({
    Name = "Fly Speed",
    Flag = "FlySection_FlySpeed",
    Value = getgenv().ScriptConfig.FlyConfig.Speed,
    Min = 10,
    Max = 200,
    Callback = function(value)
        getgenv().ScriptConfig.FlyConfig.Speed = value
    end
})

FlySection:AddSlider({
    Name = "Fly Vertical Speed",
    Flag = "FlySection_FlyVerticalSpeed",
    Value = getgenv().ScriptConfig.FlyConfig.VerticalSpeed,
    Min = 1,
    Max = 50,
    Callback = function(value)
        getgenv().ScriptConfig.FlyConfig.VerticalSpeed = value
    end
})

-- Keybind Handlers
UserInputService.InputBegan:Connect(function(input, isProcessed)
    if isProcessed then return end

    if input.KeyCode == getgenv().ScriptConfig.CameraLockConfig.ToggleKey and cameraLockToggleState then
        toggleCameraLock()
    elseif input.KeyCode == getgenv().ScriptConfig.SpeedConfig.ToggleKey and speedToggleState then
        toggleSpeed()
    elseif input.KeyCode == getgenv().ScriptConfig.FlyConfig.ToggleKey and flyToggleState then
        toggleFly()
    end
end)
