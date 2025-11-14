package com.orglead.ai.backend.service;

import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import java.util.Map;

@Service
public class LLMService {

    private final WebClient webClient;

    public LLMService() {
        this.webClient = WebClient.builder()
                .baseUrl("http://localhost:8000") // Python chatbot endpoint
                .build();
    }

    public String processInput(String userInput) {
        Mono<Map> responseMono = webClient.post()
                .uri("/chat")
                .bodyValue(Map.of("text", userInput))
                .retrieve()
                .bodyToMono(Map.class);

        Map<String, String> response = responseMono.block();
        return response != null ? response.get("response") : "Error: no response from Python bot";
    }
}
