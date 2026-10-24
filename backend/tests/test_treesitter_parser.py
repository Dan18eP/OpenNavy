import tempfile
from pathlib import Path
import pytest

from app.analyzers.treesitter_engine import TreeSitterEngine
from app.analyzers.ast_parser import UniversalASTParser


def test_treesitter_parser_typescript():
    ts_code = """
import { Request, Response } from 'express';
import * as db from '../db';
const config = require('./config');

// if (this_is_in_a_comment) { return false; }
/* while (another_fake_loop) { && || } */
const fakeString = "if (fake) { while(true) { return && ||; } }";

export function processOrder(orderId: string, priority: number): boolean {
    if (orderId && priority > 10) {
        return true;
    } else if (priority === 0 || orderId === 'admin') {
        return false;
    }
    return true;
}

export class OrderService {
    validate(id: string): boolean {
        for (let i = 0; i < 5; i++) {
            if (i === 2) {
                return false;
            }
        }
        return true;
    }
}
"""
    engine = TreeSitterEngine()
    node = engine.parse_source("src/order.ts", ts_code, "typescript")

    assert node is not None
    assert node.language == "typescript"
    assert "express" in node.imports
    assert "../db" in node.imports
    assert "./config" in node.imports

    # Clases
    assert len(node.classes) >= 1
    assert any(c.name == "OrderService" for c in node.classes)

    # Funciones
    fn_names = [fn.name for fn in node.functions]
    assert "processOrder" in fn_names
    assert "validate" in fn_names

    # McCabe Complejidad:
    # processOrder: base 1 + if(1) + &&(1) + elif/if(1) + ||(1) = 5
    # Los comentarios y strings "if (this_is_in_a_comment)..." NO deben computarse.
    proc_fn = next(fn for fn in node.functions if fn.name == "processOrder")
    assert proc_fn.cyclomatic_complexity == 5
    assert proc_fn.parameters_count == 2


def test_treesitter_ignores_comments_and_strings():
    """Verifica que palabras clave dentro de comentarios y literales no inflen la complejidad."""
    clean_code = """
function simple(): number {
    return 42;
}
"""
    noisy_code = """
// if (foo) for (bar) while (baz) case catch && ||
/*
   if (condition) {
       while (running) {}
   }
*/
const msg = "if (a && b || c) { for (;;) { while (x) { case 1: } } }";
function simple(): number {
    return 42;
}
"""
    engine = TreeSitterEngine()
    node_clean = engine.parse_source("test.ts", clean_code, "typescript")
    node_noisy = engine.parse_source("test.ts", noisy_code, "typescript")

    fn_clean = node_clean.functions[0]
    fn_noisy = node_noisy.functions[0]

    # Ambas funciones deben tener complejidad 1
    assert fn_clean.cyclomatic_complexity == 1
    assert fn_noisy.cyclomatic_complexity == 1
    # Y el archivo total debe tener complejidad 1 porque no hay bifurcaciones fuera
    assert node_clean.cyclomatic_complexity_total == 1
    assert node_noisy.cyclomatic_complexity_total == 1


def test_treesitter_parser_java():
    java_code = """
package com.praxia.service;

import java.util.List;
import java.util.Map;

public class InventoryManager {
    public int countItems(List<String> items, int threshold) {
        int count = 0;
        for (String item : items) {
            if (item != null && item.length() > threshold) {
                count++;
            }
        }
        return count;
    }
}
"""
    engine = TreeSitterEngine()
    node = engine.parse_source("InventoryManager.java", java_code, "java")

    assert node is not None
    assert node.language == "java"
    assert "java.util.List" in node.imports
    assert "java.util.Map" in node.imports
    assert len(node.classes) == 1
    assert node.classes[0].name == "InventoryManager"

    assert len(node.functions) == 1
    fn = node.functions[0]
    assert fn.name == "countItems"
    # base 1 + enhanced_for(1) + if(1) + &&(1) = 4
    assert fn.cyclomatic_complexity == 4


def test_treesitter_parser_go():
    go_code = """
package main

import (
    "fmt"
    "os"
)

type Worker struct {
    ID int
}

func Process(items []string) error {
    if len(items) == 0 {
        return nil
    }
    for i := 0; i < len(items); i++ {
        if items[i] == "" {
            continue
        }
    }
    return nil
}
"""
    engine = TreeSitterEngine()
    node = engine.parse_source("worker.go", go_code, "go")

    assert node is not None
    assert node.language == "go"
    assert "fmt" in node.imports
    assert "os" in node.imports
    assert len(node.classes) == 1
    assert node.classes[0].name == "Worker"

    assert len(node.functions) == 1
    fn = node.functions[0]
    assert fn.name == "Process"
    # base 1 + if(1) + for(1) + if(1) = 4
    assert fn.cyclomatic_complexity == 4


def test_universal_ast_parser_integration():
    """Verifica que UniversalASTParser use Tree-sitter de manera transparente."""
    with tempfile.NamedTemporaryFile("w", suffix=".ts", delete=False, encoding="utf-8") as f:
        f.write("""
import { axios } from 'axios';

// if (fake) {}
function ping(url: string): boolean {
    if (url.length > 0) {
        return true;
    }
    return false;
}
""")
        f_path = f.name

    try:
        parser = UniversalASTParser()
        node = parser.parse_file(f_path, "typescript")

        assert node.language == "typescript"
        assert "axios" in node.imports
        assert len(node.functions) == 1
        assert node.functions[0].name == "ping"
        assert node.functions[0].cyclomatic_complexity == 2  # base 1 + if(1)
        assert 0.0 <= node.maintainability_index <= 100.0
    finally:
        Path(f_path).unlink(missing_ok=True)
