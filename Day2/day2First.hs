import Data.List.Split (splitOn)
import System.IO

filt :: [String] -> [String]
filt []         = []
filt (x:xs)     = if decode x then x:(filt xs) else filt xs


decode :: String -> Bool
decode line = let
        [limits, letter, pass] = words line
        [from, to] = splitOn "-" $ limits
        in grade (read from::Int) (read to::Int) (head letter) pass
        
grade :: Int -> Int -> Char -> String -> Bool
grade from to letter pass = let 
        len = length . filter (== letter) $ pass
        in len >= from && len <= to 


main :: IO()
main = do
        input <- (fmap lines getContents) --Write this nicely later!
        let filtered = filt input
        print . length $ filtered

test1 = "ecl:ambpid:690616023byr:1994 iyr:2014 hgt:172cm hcl:#c0946f eyr:2022"

test2 = "eyr:1980 cid:97\nhcl:z ecl:#102145 iyr:2011 byr:1945\npid:187cm hgt:179in"
