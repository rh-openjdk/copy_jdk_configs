#!/usr/bin/lua
-- http://pkgs.fedoraproject.org/cgit/rpms/java-1.8.0-openjdk.git/tree/java-1.8.0-openjdk.spec#n1760
-- this file is about to be indlined in spec file, note that the copypaste in spec file may be more accurate then this one
local posix = require "posix"

local debug = true
SOURCE1 = "/home/jvanek/hg/copy_jdk_configs/copy_jdk_configs.lua"
SOURCE2 = "/usr/libexec/copy_jdk_configs.lua"

local stat1 = posix.stat(SOURCE1, "type");
local stat2 = posix.stat(SOURCE2, "type");

  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE1 .." exists - copy-jdk-configs in transaction, using this one.")
  end;
  package.path = package.path .. ";" .. SOURCE1
else 
  if (stat2 ~= nil) then
  if (debug) then
    print(SOURCE2 .." exists - copy-jdk-configs alrady installed and NOT in transation. Using.")
  end;
  package.path = package.path .. ";" .. SOURCE2
  else
    if (debug) then
      print(SOURCE1 .." does NOT exists")
      print(SOURCE2 .." does NOT exists")
      print("No config files will be copied")
    end
  os.exit(0)
  end
end
-- run contetn of included file
arg = {"--debug true"}
require "copy_jdk_configs.lua"
