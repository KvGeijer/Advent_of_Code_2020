import System.IO  
import Data.List
import Data.Maybe

createMat :: [Int] -> [[[Bool]]]
createMat list = [[[x+y+z == 2020| z <- list]| x <- list]| y <- list]

makeIntegers :: String -> [Int]
makeIntegers = (map read).lines


main :: IO ()
main = do
	inputStrings <- getContents
	let 	
		input = makeIntegers inputStrings	--Could do with fmap
		filtMat = createMat input
		flatMat = map (map or) filtMat
		flat = map or flatMat
		
		
		i = fromJust $ elemIndex True flat
		j = fromJust $ elemIndex True (flatMat !! i)
		k = fromJust $ elemIndex True ((filtMat !! i) !! j)
		first = input !! i
		second = input !! j
		third = input !! k
		mult = first * second * third
	print first
	print second
	print third
	print mult

		
		
	


	