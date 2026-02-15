# Grocery Store Till System - Developer excercise

## Solution overview
A CLI application, written in Python.

## Functionality

### Product Management
The till supports configuration of products with:
- Name (unique identifier)
- Price in clouds
- Category (e.g., "fruit", "vegetable", "bakery")

### Promotional Rules
Available discount types:

**Bundle Discount (X for Y)**
- Customer buys X items from a specified list but only pays for Y of them
- The cheapest item(s) are free
- If more items than X are scanned, only the first X items found are eligible for the discount
- Multiple separate bundles can be applied if enough items exist

**Progressive Discount (Buy X Get Next at Y% off)**
- When buying multiple of the same item, receive progressive discounts
- Can be configured for any percentage off and any quantity threshold
- Example: "Buy 1 Get 1 at 50% off" or "Buy 2 Get 1 at 25% off"

**Bulk Purchase (X or more for Y clouds each)**
- When buying X or more of the same item, each item costs Y clouds instead of the regular price
- Example: "3 or more apples for 40c each" (regular price might be 50c)

Unlimited number of discounts of any type can be added.

### Till Operations
- Scan items one at a time or in batch
- Calculate running total
- Apply promotional discounts automatically
- Display itemized receipt showing:
  - Each scanned item and its price
  - Applied discounts with savings amount
  - Final total in aws and clouds

### Configuration Interface
Administrators are able to:
- Add/remove/update products
- Create/modify/remove promotional rules
- View current product catalog and active promotions

## Discount conflict resolution logic

### Requirements
When an item qualifies for multiple discounts:
- Each item can only be part of ONE discount.
- The system should apply the discount that gives the customer the best value.

### Solution
The system applies to the item basket the combination of discounts that gives the customer the best value:
- The system generates all possible orders of discounts by generating all permutations of the list of active discounts. It then applies the discounts in the different orders to different copies of the basket. 
- On applying a discount to a basket, the system marks the items used in the discount to prevent their use for next discounts.
- After applying the discounts from all permutations, the system selects the result basket copy which has the lowest discounted price.
