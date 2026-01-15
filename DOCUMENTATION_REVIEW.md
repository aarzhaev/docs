# Documentation Review: Research Context & Interview Guide Features

## Executive Summary

This document provides a comprehensive review of the documentation for the new Research Context and Interview Guide AI Agent features. It identifies gaps, missing UX scenarios, and recommendations for improvements.

**Date:** 2025-01-17  
**Reviewer:** AI Assistant  
**Scope:** Research Context Brief generation, Interview Guide generation, AI Agent interface

---

## 1. Missing UX Scenarios and Features

### 1.1 Empty State with Suggestions ⚠️ **CRITICAL MISSING**

**What exists in code:**
- `AgentEmptyState` component shows three suggestion buttons:
  - "Create Research Context" - starts Research Context Brief generation
  - "Create Interview Guide" - starts Interview Guide generation  
  - "Ask About Service" - queries Aseed documentation

**What's missing in documentation:**
- No mention of the empty state interface
- No description of suggestion buttons
- No explanation of how to start a conversation

**Recommendation:**
Add a step in both `interviews/guide-builder.mdx` and `projects/context.mdx` describing the empty state and suggestion buttons.

---

### 1.2 Fast/Thinking Mode Selection ⚠️ **MISSING**

**What exists in code:**
- Model selector in chat input (`PromptInputModelSelect`)
- Two modes: Fast (2 tokens) and Thinking (5 tokens)
- Visual divider when mode changes (`ModelDivider`)
- Mode persists per message

**What's missing in documentation:**
- No description of HOW to switch modes in UI
- No explanation of when to use each mode
- No mention of the visual divider

**Recommendation:**
Add a section explaining:
- Where the mode selector is located (in the input area)
- How to switch between modes
- Visual indicators (divider between messages)
- When to use each mode with examples

---

### 1.3 Preview Cards (ResearchContextCard, GuideCard) ⚠️ **MISSING**

**What exists in code:**
- Cards appear in chat showing preview of generated content
- "View" button to open full panel
- Shows first 5 lines of content with line-clamp

**What's missing in documentation:**
- No mention of preview cards
- No explanation of how to view full content from card

**Recommendation:**
Add information about preview cards in the "View the generated guide/brief" steps.

---

### 1.4 Save to Project: Badges and Overwrite Confirmation ⚠️ **PARTIALLY MISSING**

**What exists in code:**
- Badges showing "Has context/guide" or "No context/guide" for each project
- Confirmation dialog when overwriting existing context/guide
- Loading states during save
- Error handling with toast notifications

**What's missing in documentation:**
- No mention of badges indicating existing content
- No explanation of overwrite confirmation
- No description of error states

**Recommendation:**
Add details about:
- What badges mean
- When confirmation is required
- What happens if save fails

---

### 1.5 Skip Questions Feature ⚠️ **PARTIALLY MISSING**

**What exists in code:**
- "Skip" button on question cards
- Sends "skip" message to agent
- Agent asks alternative questions

**What's in documentation:**
- Mentioned in Best Practices: "Skip questions if needed"

**What's missing:**
- No explanation of HOW to skip (button location)
- No description of what happens after skipping
- No examples of when to skip

**Recommendation:**
Add a dedicated section or expand Best Practices with:
- Screenshot showing Skip button
- Explanation of skip behavior
- When it's appropriate to skip

---

### 1.6 Documentation Mode (Ask About Aseed) ⚠️ **MISSING**

**What exists in code:**
- `search_documentation` tool in agent
- `DocumentationPart` in message parts
- "Documentation" tag/badge on messages
- MCP server integration for docs search

**What's missing in documentation:**
- No dedicated page or section about asking questions about Aseed
- No explanation of Documentation mode
- No mention of the "Ask About Service" suggestion

**Recommendation:**
Create a new section or page explaining:
- How to ask questions about Aseed features
- What types of questions are supported
- How documentation search works
- Examples of questions

---

### 1.7 Fallback Generation ⚠️ **MISSING**

**What exists in code:**
- `_build_fallback_markdown()` method
- Fallback activates on LLM errors
- Warning message in generated document
- "(fallback)" marker in title

**What's missing in documentation:**
- No explanation of fallback mechanism
- No mention of when fallback is used
- No description of fallback document quality

**Recommendation:**
Add a section explaining:
- What fallback generation is
- When it occurs
- How to identify fallback documents
- What to do if you get a fallback document

---

### 1.8 Validation and Follow-up Questions ⚠️ **MISSING**

**What exists in code:**
- `research_context_validator.py` validates brief structure
- Generates follow-up questions with severity (must/should)
- Prioritizes "must" questions
- Checks for conflicts and missing fields

**What's missing in documentation:**
- No explanation of validation process
- No mention of follow-up question prioritization
- No description of what validation checks

**Recommendation:**
Add information about:
- How validation works
- What follow-up questions mean
- Priority levels (must/should)
- How agent uses validation results

---

### 1.9 Providing Materials Instead of Q&A ⚠️ **MISSING**

**What exists in code:**
- Agent detects long text (>500 chars) as materials
- First message asks if user has materials
- Agent analyzes materials and extracts information
- Skips questions about already-provided info

**What's missing in documentation:**
- No mention of providing materials option
- No explanation of how to share materials
- No description of material analysis

**Recommendation:**
Add a section explaining:
- How to provide materials/documentation
- What format materials should be in
- How agent processes materials
- When to use materials vs Q&A

---

### 1.10 Cross-Suggestion (Guide → Context, Context → Guide) ⚠️ **PARTIALLY MISSING**

**What exists in code:**
- After generating guide, agent suggests creating Research Context Brief
- After generating context, agent suggests creating guide (if implemented)
- Checks for existing content before suggesting

**What's in documentation:**
- Mentioned briefly in guide-builder.mdx

**What's missing:**
- No clear explanation of the suggestion flow
- No description of when suggestions appear
- No guidance on whether to accept suggestions

**Recommendation:**
Add clear explanation of:
- When cross-suggestions appear
- What the suggestion means
- Whether to accept or decline

---

### 1.11 Modifying Existing Guides/Context ⚠️ **PARTIALLY MISSING**

**What exists in code:**
- Agent can modify existing guides/context
- `existing_guide_content` and `existing_context_content` parameters
- Agent analyzes modification requests
- Regenerates based on modifications

**What's in documentation:**
- Mentioned: "You can ask the AI to modify the guide"

**What's missing:**
- No examples of modification requests
- No explanation of how to start modification
- No description of modification process

**Recommendation:**
Add a dedicated section with:
- How to request modifications
- Examples of modification requests
- What happens during modification
- Best practices for modifications

---

### 1.12 Error Handling and Edge Cases ⚠️ **MISSING**

**What exists in code:**
- Insufficient tokens error with message
- Network errors with fallback
- JSON parsing errors with fallback extraction
- Length limit errors with partial response handling

**What's missing in documentation:**
- No error handling documentation
- No explanation of what users see on errors
- No troubleshooting guide

**Recommendation:**
Add a troubleshooting section covering:
- Insufficient tokens
- Network errors
- Generation failures
- How to retry

---

## 2. Incomplete or Incorrect Information

### 2.1 Token Cost Calculation

**Current documentation:**
- States "2 tokens per assistant message" for Fast
- States "5 tokens per assistant message" for Thinking

**Issue:**
- Doesn't clarify if this is per message or per conversation
- Doesn't explain that tokens are only for assistant messages
- Doesn't mention that user questions don't cost tokens

**Recommendation:**
Clarify:
- Tokens are charged per assistant response
- User messages/questions are free
- Each Q&A turn costs tokens
- Example: 10 questions = 10 assistant responses = 20 tokens (Fast) or 50 tokens (Thinking)

---

### 2.2 Research Context Brief Structure

**Current documentation:**
- Lists sections that are collected
- Doesn't explain the 11-section structure
- Doesn't mention validation requirements

**Recommendation:**
Add:
- Complete list of 11 sections
- Purpose of each section
- Minimum requirements (e.g., min 3 research questions)
- Validation rules

---

### 2.3 Interview Guide Structure

**Current documentation:**
- Mentions sections but not detailed structure
- Doesn't explain numbering system
- Doesn't mention follow-up questions format

**Recommendation:**
Add:
- Complete guide structure
- How questions are numbered
- Follow-up question format
- Section organization

---

## 3. Missing Screenshots and Visuals

### 3.1 Required Screenshots (from TODO comments)

**Interview Guide Builder:**
- Empty state with suggestions
- Conversation with questions
- Summary/confirmation dialog
- Generated guide in panel
- Save dropdown menu

**Research Context:**
- Empty state with suggestions
- Q&A conversation
- Generated brief in panel
- Save dropdown with project list

**General:**
- Fast/Thinking mode selector
- Model divider between messages
- Preview cards
- Badges in save menu
- Overwrite confirmation dialog
- Documentation mode tag

---

## 4. Navigation and Structure Issues

### 4.1 Missing Dedicated Pages

**Recommendation:**
Consider creating:
- `/ai-agent` or `/agent` - Overview page for AI Agent
- `/agent/documentation` - Page about asking questions about Aseed
- `/agent/troubleshooting` - Error handling and troubleshooting

---

### 4.2 Cross-References

**Issues:**
- Some cross-references are missing
- Links between related features could be improved

**Recommendation:**
Add more cross-references:
- From guide-builder to context (and vice versa)
- From both to token usage
- From token usage to both features

---

## 5. Best Practices Gaps

### 5.1 Missing Best Practices

**Recommendation:**
Add best practices for:
- When to use Fast vs Thinking mode
- When to provide materials vs answer questions
- How to structure materials for best results
- When to skip questions
- How to request effective modifications
- How to combine guide and context generation

---

## 6. Technical Details Missing

### 6.1 Agent Behavior

**Missing:**
- How agent determines when to ask next question
- How agent decides when enough information is collected
- How agent handles ambiguous answers
- How agent adapts to user's language

**Recommendation:**
Add a "How it works" section explaining agent decision-making.

---

### 6.2 Validation Details

**Missing:**
- What validation checks are performed
- What "must" vs "should" follow-ups mean
- How validation affects generation

**Recommendation:**
Add validation details to Research Context documentation.

---

## 7. Priority Recommendations

### High Priority (Must Add)

1. **Empty State and Suggestions** - Critical for first-time users
2. **Fast/Thinking Mode Selection** - Core feature, needs UI explanation
3. **Save to Project: Badges and Overwrite** - Important UX detail
4. **Documentation Mode** - Major feature, completely missing
5. **Providing Materials** - Alternative workflow, not documented

### Medium Priority (Should Add)

6. **Preview Cards** - Important UX element
7. **Skip Questions** - Useful feature, needs better documentation
8. **Modification Process** - Mentioned but not detailed
9. **Fallback Generation** - Users should know about this
10. **Validation and Follow-ups** - Technical but important

### Low Priority (Nice to Have)

11. **Cross-suggestions** - Already mentioned, could expand
12. **Error Handling** - Troubleshooting guide
13. **Technical Details** - For advanced users

---

## 8. Specific File Updates Needed

### 8.1 `interviews/guide-builder.mdx`

**Add:**
- Step about empty state and suggestions
- Section on Fast/Thinking mode selection (with UI screenshot)
- Information about preview cards
- Details about Skip button
- Expanded modification section with examples
- Cross-suggestion explanation

### 8.2 `projects/context.mdx`

**Add:**
- Step about empty state and suggestions
- Section on Fast/Thinking mode selection (with UI screenshot)
- Information about preview cards
- Details about providing materials
- Validation and follow-up questions explanation
- Fallback generation information
- Expanded modification section

### 8.3 `account/usage.mdx`

**Already updated** - Good coverage of AI Agent costs

### 8.4 New Files to Create

**Consider:**
- `agent/overview.mdx` - General AI Agent overview
- `agent/documentation.mdx` - Asking questions about Aseed
- `agent/troubleshooting.mdx` - Error handling

---

## 9. Screenshot Requirements

### 9.1 Critical Screenshots Needed

1. **Empty State:**
   - File: `images/agent-empty-state-light.png` / `-dark.png`
   - Shows three suggestion buttons

2. **Mode Selector:**
   - File: `images/agent-mode-selector-light.png` / `-dark.png`
   - Shows Fast/Thinking dropdown in input area

3. **Model Divider:**
   - File: `images/agent-model-divider-light.png` / `-dark.png`
   - Shows divider between messages when mode changes

4. **Preview Card:**
   - File: `images/agent-guide-card-light.png` / `-dark.png`
   - Shows preview card with View button

5. **Save Menu with Badges:**
   - File: `images/agent-save-menu-badges-light.png` / `-dark.png`
   - Shows dropdown with projects and badges

6. **Overwrite Confirmation:**
   - File: `images/agent-overwrite-confirmation-light.png` / `-dark.png`
   - Shows confirmation dialog

7. **Documentation Mode:**
   - File: `images/agent-documentation-mode-light.png` / `-dark.png`
   - Shows message with Documentation tag

---

## 10. Content Improvements

### 10.1 Language and Tone

**Issues:**
- Some sections are too technical
- Missing user-friendly explanations
- Not enough examples

**Recommendation:**
- Add more examples throughout
- Use simpler language where possible
- Include "What you'll see" descriptions

### 10.2 Step-by-Step Clarity

**Issues:**
- Some steps assume prior knowledge
- Missing "what happens next" explanations

**Recommendation:**
- Add "What happens next" to each step
- Include expected outcomes
- Add troubleshooting tips in steps

---

## 11. Testing Recommendations

### 11.1 User Testing Scenarios

**Test these scenarios are documented:**
1. First-time user creating guide
2. First-time user creating context
3. User providing materials
4. User skipping questions
5. User modifying existing guide
6. User switching modes mid-conversation
7. User saving to project with existing content
8. User asking about Aseed features

---

## 12. Summary of Actions

### Immediate Actions (Critical)

1. ✅ Add empty state documentation
2. ✅ Add Fast/Thinking mode UI explanation
3. ✅ Add save menu badges and overwrite confirmation
4. ✅ Create documentation mode section
5. ✅ Add materials provision workflow

### Short-term Actions (Important)

6. Add preview cards explanation
7. Expand skip questions documentation
8. Add fallback generation information
9. Add validation details
10. Create troubleshooting guide

### Long-term Actions (Enhancement)

11. Create dedicated AI Agent overview page
12. Add technical details section
13. Expand best practices
14. Add more examples throughout

---

## Conclusion

The documentation covers the basic workflows but misses many important UX details and edge cases. The most critical gaps are:

1. **Empty state and suggestions** - Users won't know how to start
2. **Mode selection UI** - Core feature not explained
3. **Documentation mode** - Major feature completely missing
4. **Save workflow details** - Important UX not documented
5. **Materials provision** - Alternative workflow missing

Priority should be given to documenting the user interface elements and interaction patterns, as these are essential for users to successfully use the features.
