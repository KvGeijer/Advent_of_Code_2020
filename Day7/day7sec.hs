import System.IO
import Data.List.Split (splitOn)
import Data.List (nub, union, intersect, elemIndex)
import Data.Maybe
import Data.Array

--Should probably use a hash set to improve speed...

--Too low!
main = do
        rules <- fmap (map toRules . lines . filter (/= '\r')) getContents
        let bags = solve rules
        print bags

-- How many bags must the shiny gold bag contain?
solve :: [(String, [(Int, String)])] -> Int
solve rules = nbrBags "shiny gold bag" rules

-- Use dynamic programming
nbrBags :: String -> [(String, [(Int, String)])] -> Int
nbrBags search rules = optArray ! (myIndex search bagIndexes) where
        --Should really create a bagIndexArray for better time
        standAloneRules :: [ [(Int, String)] ]
        (bagIndexes, standAloneRules) = unzip rules
        n = length bagIndexes
        
        optArray   = listArray (0,n-1) [opt bag | bag <- bagIndexes]
        
        -- How many bags are in this one?
        opt :: String -> Int
        opt [] = 0
        opt bag = sum . map opt2 $ (standAloneRules !! (myIndex bag bagIndexes))
        
        --This one includes the actual bag and all the bags inside of it.
        opt2 :: (Int, String) -> Int
        opt2 (num, []) = num*1;
        opt2 (num, content) = num + num * (optArray ! ind) where 
                ind = myIndex content bagIndexes
        
        

toRules :: String -> (String, [(Int, String)])
toRules line = let
         [bags, contents] = splitOn " contain " line
         bag = bagsToBag bags
         rules = map (separateNumbers . bagsToBag) . splitOn ", " $ init contents
         in (bag, if contents /= "no other bags." then rules else [])
         
separateNumbers :: String -> (Int, String)
separateNumbers rule = let 
        bag = tail . dropWhile (/= ' ') $ rule
        num = read . takeWhile (/= ' ') $ rule
        in (num, bag)

myIndex :: Eq a => a -> [a] -> Int
myIndex s = fromJust . elemIndex s

bagsToBag :: String -> String
bagsToBag bags = if last bags == 's' then init bags else bags