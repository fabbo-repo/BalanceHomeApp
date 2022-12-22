

import 'package:balance_home_app/src/core/providers/localization/localization_provider.dart';
import 'package:balance_home_app/src/features/balance/data/models/balance_limit_type_enum.dart';
import 'package:balance_home_app/src/features/balance/data/models/balance_type_enum.dart';
import 'package:balance_home_app/src/features/balance/logic/providers/balance_provider.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

class BalanceLimitTypeDialog extends ConsumerWidget {
  final BalanceTypeEnum balanceType;

  const BalanceLimitTypeDialog({
    required this.balanceType,
    super.key
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final balanceLimitTypeNotifier = (balanceType == BalanceTypeEnum.expense) ?
      ref.read(expenseLimitTypeStateNotifierProvider.notifier) : 
      ref.read(revenueLimitTypeStateNotifierProvider.notifier);
    BalanceLimitTypeEnum currentType = (balanceType == BalanceTypeEnum.expense) ?
      ref.watch(expenseLimitTypeStateNotifierProvider).limitType :
      ref.watch(revenueLimitTypeStateNotifierProvider).limitType;
    final appLocalizations = ref.read(localizationStateNotifierProvider).localization;
    return AlertDialog(
      title: (balanceType == BalanceTypeEnum.expense) ?
        Text(appLocalizations.maxExpenseDialoTitle) :
        Text(appLocalizations.maxRevenueDialoTitle),
      content: SingleChildScrollView(
        child: SizedBox(
          width: double.infinity,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              BalanceLimitTypeEnum.limit5,
              BalanceLimitTypeEnum.limit15,
              BalanceLimitTypeEnum.none,
            ]
              .map((e) => RadioListTile(
                title: Text(
                  (e == BalanceLimitTypeEnum.limit5) ? 
                    "5" :
                      (e == BalanceLimitTypeEnum.limit15) ?
                        "15" :
                          appLocalizations.noLimit
                ),
                value: e,
                groupValue: currentType,
                selected: currentType == e,
                onChanged: (value) {
                  if (value != currentType) {
                    Navigator.pop(context);
                    balanceLimitTypeNotifier.setLimitType(e);
                  }
                },
              ))
              .toList(),
          ),
        ),
      ));
  }
}