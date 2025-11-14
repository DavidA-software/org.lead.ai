package com.orglead.ai.backend.controller;

import com.orglead.ai.backend.service.LLMService;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class LLMController {

    private final LLMService llmService;

    public LLMController(LLMService llmService) {
        this.llmService = llmService;
    }

    @PostMapping("/chat")
    public String chat(@RequestBody String prompt) {
        return llmService.processInput(prompt);
    }
}
