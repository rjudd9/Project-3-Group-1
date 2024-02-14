// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract EliteEats is ERC721, Ownable(msg.sender) {
    uint256 public tokenCounter;
    uint256 public constant maxTokens = 10; // Maximum number of tokens that can be minted
    //Allows minting of one token per Wallet
    mapping(address => bool) public hasMinted;
    mapping(uint256 => string) public tokenURIs; // Mapping from token ID to image URI

    // Event to emit when a new NFT is minted
    event NFTMinted(address indexed owner, uint256 indexed tokenId);

    // Constructor function
    constructor() ERC721("EliteEats", "ELT") {}

    // Function to mint a new NFT
    function mintNFT() external {
        require(tokenCounter < maxTokens, "Maximum number of tokens minted");
        require(!hasMinted[msg.sender], "You have already minted a token");
        
        uint256 tokenId = tokenCounter;
        _safeMint(msg.sender, tokenId);
        tokenCounter++;
        hasMinted[msg.sender] = true;
        
        emit NFTMinted(msg.sender, tokenId);
    }

    // Function to allow transfer of tokens by the owner
    function transferToken(address to, uint256 tokenId) external onlyOwner {
        _transfer(owner(), to, tokenId);
    }

    // Function to check the total supply of tokens
    function totalSupply() external view returns (uint256) {
        return tokenCounter;
    }
   // Fallback function to receive Ether
    receive() external payable {}

    // Fallback function to receive Ether
    fallback() external payable {}


}


