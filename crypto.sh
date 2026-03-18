#!/bin/bash
#
# Crypto Data CLI - Shell wrapper for cryptocurrency market data and analysis
#
# Usage:
#   ./crypto.sh <command> [options]
#
# Commands:
#   candles <inst_id> [options]           Get K-line/OHLCV data
#   funding-rate <inst_id> [options]      Get funding rate
#   open-interest <inst_id> [options]     Get open interest
#   long-short-ratio <ccy> [options]      Get long/short ratio
#   liquidation <inst_id> [options]       Get liquidation orders
#   top-trader-ratio <inst_id> [options]  Get top trader position ratio
#   option-ratio <ccy> [options]          Get option call/put ratio
#   fear-greed [options]                  Get Fear and Greed Index
#   indicators <inst_id> [options]        Get technical indicators
#   summary <inst_id> [options]           Get analysis summary
#   support-resistance <inst_id> [options] Get support/resistance levels
#
# Examples:
#   ./crypto.sh candles BTC-USDT --bar 1H --limit 100
#   ./crypto.sh funding-rate BTC-USDT-SWAP --limit 50
#   ./crypto.sh indicators ETH-USDT --bar 4H --last-n 5
#   ./crypto.sh fear-greed --days 30
#

# Resolve script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Set Python encoding
export PYTHONIOENCODING=utf-8

# Run CLI
exec python "$SCRIPT_DIR/scripts/cli.py" "$@"