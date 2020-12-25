import Data.List.Split (splitOn)
import System.IO

filt :: [String] -> [String]
filt []         = []
filt (x:xs)     = if decode x then x:(filt xs) else filt xs


decode :: String -> Bool
decode line = let
        [limits, letter, pass] = words line
        [from, to] = splitOn "-" limits
        in grade (read from::Int) (read to::Int) (head letter) pass
        
grade :: Int -> Int -> Char -> String -> Bool
grade from to letter pass = (first || second) && not (first && second) where
        first = pass !! (from-1) == letter
        second = pass !! (to-1) == letter


main :: IO()
main = do
        input <- (fmap lines getContents) --Write this nicely later!
        let filtered = filt input
        print . length $ filtered