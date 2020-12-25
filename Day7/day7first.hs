import System.IO
import Data.List.Split (splitOn)
import Data.List (nub, union, intersect)
import Data.Array

--Should probably use a hash set to improve speed...

main = do
        rules <- fmap (map toRules . lines . filter (/= '\r')) getContents
        let bags = solve rules
        --mapM putStrLn bags
        print . length $  bags


solve :: [(String, [String])] -> [String]
solve rules = recSol [] ["shiny gold bag"] rules

-- iterate until you find a fix point
recSol :: [String] -> [String] -> [(String, [String])] -> [String]
recSol found list rules = let 
        newList = nub $ findBags found list rules 
        in if newList /= [] then recSol (newList ++ found) newList rules else found

-- output all bags which can contain the ones in bags, but are not in earlier
findBags :: [String] -> [String] -> [(String, [String])] -> [String]
findBags earlier bags [] = []
findBags earlier bags ((bag, cont):xs) = let rest = findBags earlier bags xs in if (not (elem bag earlier) && intersect bags cont /= [])
        then bag : rest
        else rest                   --No new information, just continue
--findBags earlier bags ((bag, cont):xs) = let newBags = filter (\x -> (elem x bags) && (not $ elem x earlier)) cont
--        in newBags ++ findBags earlier bags xs


toRules :: String -> (String, [String])
toRules line = let
         [bags, contents] = splitOn " contain " line
         bag = bagsToBag bags
         rules = map (removeNumbers . bagsToBag) . splitOn ", " $ init contents
         in (bag, if contents /= "no other bags." then rules else [])
         
removeNumbers :: String -> String
removeNumbers = tail . dropWhile (/= ' ')         

bagsToBag :: String -> String
bagsToBag bags = if last bags == 's' then init bags else bags